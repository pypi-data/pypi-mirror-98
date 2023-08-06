/*---------------------------------------------------------------------------------*/
/*  NOMAD - Nonlinear Optimization by Mesh Adaptive Direct Search -                */
/*                                                                                 */
/*  NOMAD - Version 4.0.0 has been created by                                      */
/*                 Viviane Rochon Montplaisir  - Polytechnique Montreal            */
/*                 Christophe Tribes           - Polytechnique Montreal            */
/*                                                                                 */
/*  The copyright of NOMAD - version 4.0.0 is owned by                             */
/*                 Charles Audet               - Polytechnique Montreal            */
/*                 Sebastien Le Digabel        - Polytechnique Montreal            */
/*                 Viviane Rochon Montplaisir  - Polytechnique Montreal            */
/*                 Christophe Tribes           - Polytechnique Montreal            */
/*                                                                                 */
/*  NOMAD v4 has been funded by Rio Tinto, Hydro-Québec, NSERC (Natural            */
/*  Sciences and Engineering Research Council of Canada), InnovÉÉ (Innovation      */
/*  en Énergie Électrique) and IVADO (The Institute for Data Valorization)         */
/*                                                                                 */
/*  NOMAD v3 was created and developed by Charles Audet, Sebastien Le Digabel,     */
/*  Christophe Tribes and Viviane Rochon Montplaisir and was funded by AFOSR       */
/*  and Exxon Mobil.                                                               */
/*                                                                                 */
/*  NOMAD v1 and v2 were created and developed by Mark Abramson, Charles Audet,    */
/*  Gilles Couture, and John E. Dennis Jr., and were funded by AFOSR and           */
/*  Exxon Mobil.                                                                   */
/*                                                                                 */
/*  Contact information:                                                           */
/*    Polytechnique Montreal - GERAD                                               */
/*    C.P. 6079, Succ. Centre-ville, Montreal (Quebec) H3C 3A7 Canada              */
/*    e-mail: nomad@gerad.ca                                                       */
/*                                                                                 */
/*  This program is free software: you can redistribute it and/or modify it        */
/*  under the terms of the GNU Lesser General Public License as published by       */
/*  the Free Software Foundation, either version 3 of the License, or (at your     */
/*  option) any later version.                                                     */
/*                                                                                 */
/*  This program is distributed in the hope that it will be useful, but WITHOUT    */
/*  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or          */
/*  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License    */
/*  for more details.                                                              */
/*                                                                                 */
/*  You should have received a copy of the GNU Lesser General Public License       */
/*  along with this program. If not, see <http://www.gnu.org/licenses/>.           */
/*                                                                                 */
/*  You can find information on the NOMAD software at www.gerad.ca/nomad           */
/*---------------------------------------------------------------------------------*/

#include "../../Algos/CacheInterface.hpp"
#include "../../Algos/EvcInterface.hpp"
#include "../../Algos/PhaseOne/PhaseOne.hpp"
#include "../../Cache/CacheBase.hpp"
#include "../../Eval/ComputeSuccessType.hpp"
#include "../../Output/OutputDirectToFile.hpp"

NOMAD::BBOutputTypeList NOMAD::PhaseOne::_bboutputtypes;

void NOMAD::PhaseOne::init()
{
    _name = "Phase One";
    verifyParentNotNull();

}

void NOMAD::PhaseOne::startImp()
{

    // Setup EvalPoint success computation to be based on h rather than f.
    NOMAD::EvcInterface::getEvaluatorControl()->setComputeSuccessTypeFunction(NOMAD::ComputeSuccessType::computeSuccessTypePhaseOne);
    // These are two static methods that should be un-staticized. Issue #410
    NOMAD::Eval::setComputeSuccessTypeFunction(NOMAD::Eval::computeSuccessTypePhaseOne);
    NOMAD::Eval::setComputeHFunction(NOMAD::Eval::computeHPB);

    // The cache may not be empty.
    // Recompute the h for cache points that were read from cache file.
    NOMAD::CacheBase::getInstance()->processOnAllPoints(NOMAD::PhaseOne::recomputeHPB);

    // Temporarily disable solution file (restored in endImp())
    NOMAD::OutputDirectToFile::getInstance()->disableSolutionFile();

    // Comment to appear at the end of stats lines
    setAlgoComment("(Phase One)", true); // true: force comment

    // Setup the pb parameters to stop once a feasible point is obtained
    _pbParams->setAttributeValue("STOP_IF_FEASIBLE", true);
    _pbParams->checkAndComply();


    // Setup Mads
    _madsStopReasons = std::make_shared<NOMAD::AlgoStopReasons<NOMAD::MadsStopType>>();
    _mads = std::make_shared<NOMAD::Mads>(this, _madsStopReasons, _runParams, _pbParams);

}

void NOMAD::PhaseOne::readInformationForHotRestart()
{
}



bool NOMAD::PhaseOne::runImp()
{
    bool ret = false;

    // Run Mads on Phase One.
    _mads->start();
    ret = _mads->run();
    _mads->end();

    return ret;
}


void NOMAD::PhaseOne::endImp()
{
    // Ensure evaluation of queue will continue
    NOMAD::EvcInterface::getEvaluatorControl()->restart();

    // reset to the previous stats comment
    resetPreviousAlgoComment(true); // true: release lock on comment

    // Re-enable writing in Solution file
    NOMAD::OutputDirectToFile::getInstance()->enableSolutionFile();

    // Reset success computation function
    NOMAD::EvcInterface::getEvaluatorControl()->setComputeSuccessTypeFunction(NOMAD::ComputeSuccessType::defaultComputeSuccessType);
    // These are two static methods that should be un-staticized. Issue #410
    NOMAD::Eval::setComputeSuccessTypeFunction(NOMAD::Eval::defaultComputeSuccessType);
    NOMAD::Eval::setComputeHFunction(NOMAD::Eval::defaultComputeH);

    // All points in the cache must be recomputed for their h.
    // Note: Cache is ordered on the Point part only, and we recompute the Eval
    // part, so the cache remains coherent.
    NOMAD::CacheBase::getInstance()->processOnAllPoints(NOMAD::PhaseOne::recomputeH);

    bool hasFeas = NOMAD::CacheBase::getInstance()->hasFeas();
    if (!hasFeas)
    {
        // If cache is not used, feasible points remain in the barrier
        auto barrier = _mads->getMegaIterationBarrier();
        if (nullptr != barrier)
        {
            hasFeas = (nullptr != barrier->getFirstXFeas());
        }
    }

    if (hasFeas)
    {
        std::vector<NOMAD::EvalPoint> evalPointList;
        NOMAD::CacheInterface cacheInterface(this);
        size_t numFeas = cacheInterface.findBestFeas(evalPointList, EvalType::BB, nullptr);
        if (numFeas>0)
        {
            // Evaluation info for output
            NOMAD::StatsInfo info;

            info.setBBO(evalPointList[0].getBBO(NOMAD::EvalType::BB));
            info.setSol(*(evalPointList[0].getX()));

            NOMAD::OutputDirectToFile::Write(info,true,false); // Write in solution (if solution_file exists) but not in history file
        }
    }

    // Update PhaseOne stop reasons
    auto PhaseOneStopReasons = NOMAD::AlgoStopReasons<NOMAD::PhaseOneStopType>::get( _stopReasons );
    if (!hasFeas)
    {
        if ( _madsStopReasons->checkTerminate() )
        {
            PhaseOneStopReasons->set ( NOMAD::PhaseOneStopType::MADS_FAIL );
        }
        else
        {
            PhaseOneStopReasons->set ( NOMAD::PhaseOneStopType::NO_FEAS_PT );
        }
    }
}


void NOMAD::PhaseOne::recomputeH(NOMAD::EvalPoint& evalPoint)
{
    // EvalType BB: Never use Sgte in Phase One
    auto eval = evalPoint.getEval(NOMAD::EvalType::BB);
    if (nullptr != eval && !eval->getBBO().empty())
    {
        eval->setH(NOMAD::Eval::defaultComputeH(*eval, _bboutputtypes));
    }
}


void NOMAD::PhaseOne::recomputeHPB(NOMAD::EvalPoint& evalPoint)
{
    auto eval = evalPoint.getEval(NOMAD::EvalType::BB);
    if (nullptr != eval && !eval->getBBO().empty())
    {
        eval->setH(NOMAD::Eval::computeHPB(*eval, _bboutputtypes));
    }
}
