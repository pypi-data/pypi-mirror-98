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

//#include "../../Algos/Mads/GMesh.hpp" // Code using GMesh is commented out
#include "../../Algos/Mads/Mads.hpp"
#include "../../Algos/Mads/MadsMegaIteration.hpp"
#include "../../Algos/Mads/MadsUpdate.hpp"
#include "../../Algos/Mads/MegaSearchPoll.hpp"
#include "../../Output/OutputQueue.hpp"


void NOMAD::MadsMegaIteration::init()
{
    _name = NOMAD::MegaIteration::getName();
}


void NOMAD::MadsMegaIteration::startImp()
{
    // Create a NOMAD::MadsIteration for each frame center and each desired mesh size.
    // Use all xFeas and xInf available.
    // For now, not using other frame centers.
    size_t k = _k;  // Main iteration counter

    // Update main mesh and barrier.
    NOMAD::MadsUpdate update( this );
    update.start();
    update.run();
    update.end();

    // Now that update has used the previous MegaIteration success type, reset it
    setSuccessType(NOMAD::SuccessType::NOT_EVALUATED);

    // Verify mesh stop conditions.
    _mainMesh->checkMeshForStopping( _stopReasons );

    OUTPUT_DEBUG_START
    AddOutputDebug("Mesh Stop Reason: " + _stopReasons->getStopReasonAsString());
    OUTPUT_DEBUG_END
    if ( ! _stopReasons->checkTerminate() )
    {
        // MegaIteration's barrier member is already in sub dimension.
        auto allXFeas = _barrier->getAllXFeas();
        auto allXInf  = _barrier->getAllXInf();

        // Compute the number of xFeas and xInf points we want to use, to get at
        // most MAX_ITERATION_PER_MEGAITERATION iterations.
        auto maxXFeas = allXFeas.size();
        auto maxXInf = allXInf.size();
        computeMaxXFeasXInf(maxXFeas, maxXInf);

        size_t nbPoints = 0;
        std::vector<NOMAD::EvalPoint>::const_iterator it;
        for (it = allXFeas.begin(), nbPoints = 0; it != allXFeas.end() && nbPoints < maxXFeas; ++it, nbPoints++)
        {
            std::shared_ptr<NOMAD::MadsIteration> madsIteration = std::make_shared<NOMAD::MadsIteration>(this , std::make_shared<NOMAD::EvalPoint>(*it), k, _mainMesh);
            _iterList.push_back(madsIteration);
            k++;
        }
        for (it = allXInf.begin(), nbPoints = 0; it != allXInf.end() && nbPoints < maxXInf; ++it, nbPoints++)
        {
            std::shared_ptr<NOMAD::MadsIteration> madsIteration = std::make_shared<NOMAD::MadsIteration>(this, std::make_shared<NOMAD::EvalPoint>(*it), k, _mainMesh);
            _iterList.push_back(madsIteration);
            k++;
        }

        // Add iteration for larger meshes (see issue (feature) #386)
        /*
        if (xFeasDefined)
        {
            addIterationsForLargerMeshes(xFeas, k);
        }
        if (xInfDefined)
        {
            addIterationsForLargerMeshes(xInf, k);
        }
        */

        size_t nbIter = _iterList.size();

        OUTPUT_INFO_START
        AddOutputInfo(_name + " has " + NOMAD::itos(nbIter) + " iteration" + ((nbIter > 1)? "s" : "") + ".");
        OUTPUT_INFO_END

        OUTPUT_DEBUG_START
        AddOutputDebug("Iterations generated:");
        for (size_t i = 0; i < nbIter; i++)
        {
            // downcast from Iteration to MadsIteration
            std::shared_ptr<NOMAD::MadsIteration> madsIteration = std::dynamic_pointer_cast<NOMAD::MadsIteration>( _iterList[i] );

            if ( madsIteration == nullptr )
            {
                throw NOMAD::Exception(__FILE__, __LINE__, "Invalid shared pointer cast");
            }

            AddOutputDebug( _iterList[i]->getName());
            NOMAD::ArrayOfDouble meshSize  = madsIteration->getMesh()->getdeltaMeshSize();
            NOMAD::ArrayOfDouble frameSize = madsIteration->getMesh()->getDeltaFrameSize();
            auto frameCenter = madsIteration->getFrameCenter();
            AddOutputDebug("Frame center: " + frameCenter->display());
            auto previousFrameCenter = frameCenter->getPointFrom();
            AddOutputDebug("Previous frame center: " + (previousFrameCenter ? previousFrameCenter->display() : "NULL"));
            AddOutputDebug("Mesh size:  " + meshSize.display());
            AddOutputDebug("Frame size: " + frameSize.display());
        }
        OUTPUT_DEBUG_END
    }
}


// Add iteration for larger meshes (see issue (feature) #386)
/*
bool NOMAD::MadsMegaIteration::addIterationsForLargerMeshes(const NOMAD::EvalPoint& x0, size_t &k)
{
    bool newMesh = false;

    // Compute new directions for x0, to enlarge mesh.
    size_t dim = _mainMesh->getSize();
    for (size_t i = 0; i < 2 * dim; i++)
    {
        // i = 0..dim-1 : going up
        // i = dim.. 2*dim-1 : going down
        size_t ii = (i < dim) ? i : i - dim;
        NOMAD::EvalPoint dirPoint(x0);
        NOMAD::Double delta = _mainMesh->getDeltaFrameSize(ii);
        dirPoint[ii] += delta;
        NOMAD::Direction dir = NOMAD::Point::vectorize(x0, dirPoint);

        // Create larger mesh.
        const auto largeMeshRef = std::shared_ptr<NOMAD::MeshBase>
            (new NOMAD::GMesh(*(dynamic_cast<NOMAD::GMesh*>(_mainMesh.get()))));
        auto largeMesh = std::shared_ptr<NOMAD::MeshBase>
            (new NOMAD::GMesh(*(dynamic_cast<NOMAD::GMesh*>(largeMeshRef.get()))));
        auto anisotropyFactor = _runParams->getAttributeValue<NOMAD::Double>("ANISOTROPY_FACTOR");
        bool anisotropicMesh = _runParams->getAttributeValue<bool>("ANISOTROPIC_MESH");

        if (largeMesh->enlargeDeltaFrameSize(dir, anisotropyFactor, anisotropicMesh))
        {
            // At least one new mesh was generated.
            newMesh = true;
            //std::string dirStr = "New direction " + dir.display();
            //AddOutputInfo(dirStr);
            std::shared_ptr<NOMAD::MadsIteration> madsIteration = std::make_shared<NOMAD::MadsIteration>(this, std::make_shared<NOMAD::EvalPoint>(dirPoint), k, largeMesh);
            _iterList.push_back(madsIteration);
            k++;

            // Reset largeMesh - Actually create a new one.
            largeMesh = std::shared_ptr<NOMAD::MeshBase>
                (new NOMAD::GMesh(*(dynamic_cast<NOMAD::GMesh*>(largeMeshRef.get()))));
        }

    }

    return newMesh;
}
*/


bool NOMAD::MadsMegaIteration::runImp()
{
    NOMAD::SuccessType bestSuccessYet = NOMAD::SuccessType::NOT_EVALUATED;

    std::string s;

    if ( _stopReasons->checkTerminate() )
    {
        OUTPUT_DEBUG_START
        s = "MegaIteration: stopReason = " + _stopReasons->getStopReasonAsString() ;
        AddOutputDebug(s);
        OUTPUT_DEBUG_END
        return false;
    }

    if (_iterList.empty())
    {
        throw NOMAD::Exception(__FILE__, __LINE__, "No iterations to run");
    }

    if (_runParams->getAttributeValue<bool>("GENERATE_ALL_POINTS_BEFORE_EVAL"))
    {
        MegaSearchPoll megaStep( this );
        megaStep.start();

        bool successful = megaStep.run();

        megaStep.end();

        if (successful)
        {
            bestSuccessYet = _megaIterationSuccess;
            OUTPUT_DEBUG_START
            s = _name + ": new success " + NOMAD::enumStr(bestSuccessYet);
            s += " stopReason = " + _stopReasons->getStopReasonAsString() ;
            AddOutputDebug(s);
            OUTPUT_DEBUG_END
        }

        // Note: Delta (frame size) will be updated in the Update step next time it is called.

        // End of running all the iterations
        // Update number of iterations - note: _k is atomic
        _k += _iterList.size();

    }
    else
    {
        bool iterSuccessful = false;    // Is the iteration successful.
        // Break as soon as an iteration is successful (full success only).
        for (size_t i = 0; i < _iterList.size(); i++)
        {
            // Get Mads ancestor to call terminate(k)
            NOMAD::Mads* mads = getParentOfType<NOMAD::Mads*>();
            if (nullptr == mads)
            {
                throw NOMAD::Exception(__FILE__, __LINE__, "Mads MegaIteration without Mads ancestor");
            }
            if (_stopReasons->checkTerminate()
                || iterSuccessful
                || mads->terminate(_iterList[i]->getK()))
            {
                break;
            }

            // downcast from Iteration to MadsIteration
            std::shared_ptr<NOMAD::MadsIteration> madsIteration = std::dynamic_pointer_cast<NOMAD::MadsIteration>(_iterList[i]);

            if (madsIteration == nullptr)
            {
                throw NOMAD::Exception(__FILE__, __LINE__, "Invalid shared pointer cast");
            }

            madsIteration->start();

            iterSuccessful = madsIteration->run();
            // Compute MegaIteration success
            NOMAD::SuccessType iterSuccess = madsIteration->getSuccessType();
            if (iterSuccess > bestSuccessYet)
            {
                bestSuccessYet = iterSuccess;
            }

            madsIteration->end();

            if (iterSuccessful)
            {
                OUTPUT_DEBUG_START
                s = _name + ": new success " + NOMAD::enumStr(iterSuccess);
                AddOutputDebug(s);
                OUTPUT_DEBUG_END
            }

            // Update MegaIteration's stop reason
            if (_stopReasons->checkTerminate())
            {
                OUTPUT_DEBUG_START
                s = _name + " stop reason set to: " + _stopReasons->getStopReasonAsString();
                AddOutputDebug(s);
                OUTPUT_DEBUG_END
            }

            _nbIterRun++; // Count one more iteration.

            if (_userInterrupt)
            {
                hotRestartOnUserInterrupt();
            }

        }
    }

    // MegaIteration is a success if either a better xFeas or
    // a dominating or partial success for xInf was found.
    // See Algorithm 12.2 from DFBO.
    setSuccessType(bestSuccessYet);

    // return true if we have a partial or full success.
    return (bestSuccessYet >= NOMAD::SuccessType::PARTIAL_SUCCESS);
}


void NOMAD::MadsMegaIteration::display(std::ostream& os) const
{
    os << "MAIN_MESH " << std::endl;
    os << *_mainMesh ;
    NOMAD::MegaIteration::display(os);
}


void NOMAD::MadsMegaIteration::read(std::istream& is)
{
    // Set up structures to gather member info
    size_t k = 0;
    // Read line by line
    std::string name;
    while (is >> name && is.good() && !is.eof())
    {
        if ("MAIN_MESH" == name)
        {
            if (nullptr != _mainMesh)
            {
                is >> *_mainMesh;
            }
            else
            {
                std::string err = "Error: Reading a mesh onto a NULL pointer";
                std::cerr << err;
            }
        }
        else if ("ITERATION_COUNT" == name)
        {
            is >> k;
        }
        else if ("BARRIER" == name)
        {
            if (nullptr != _barrier)
            {
                is >> *_barrier;
            }
            else
            {
                std::string err = "Error: Reading a Barrier onto a NULL pointer";
                std::cerr << err;
            }
        }
        else
        {
            for (size_t i = 0; i < name.size(); i++)
            {
                is.unget();
            }
            break;
        }
    }

    setK(k);
}


std::ostream& NOMAD::operator<<(std::ostream& os, const NOMAD::MadsMegaIteration& megaIteration)
{
    megaIteration.display ( os );
    return os;
}


std::istream& NOMAD::operator>>(std::istream& is, NOMAD::MadsMegaIteration& megaIteration)
{
    megaIteration.read(is);
    return is;
}
