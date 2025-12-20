/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) 2022-2023 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "DirACFoamWallSimple.H"
#include "fvcGrad.H"
#include "fvmDiv.H"
#include "fvmLaplacian.H"

#include "fvcSmooth.H"
#include "fvcSurfaceIntegrate.H"
#include "fvcLaplacian.H"

// * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * * //

void Foam::solvers::DirACFoamWallSimple::thermophysicalPredictor()
{

    //Make references to all volume field variables
    volScalarField& Xv(Xv_);



    //Solve for vapor transport
    fvScalarMatrix XvEqn =
    (
        fvm::ddt(Xv)
      + fvm::div(phi,Xv)
      ==
        fvm::laplacian((1/(1 + (lam/(r0*sqrt((1-Xs-Xa-Xl)/(1-Xs-Xa))))))*D0/(tau*tau),Xv)
    );

    XvEqn.relax();

    fvConstraints().constrain(XvEqn);

    XvEqn.solve("Xv");

    fvConstraints().constrain(Xv);



    volScalarField diffXv = fvc::laplacian((1/(1 + (lam/(r0*sqrt((1-Xs-Xa-Xl)/(1-Xs-Xa))))))*D0/(tau*tau),Xv);

    dXvAvg = gAverage(diffXv)*runTime.deltaTValue();
    dXvNum = max(gMax(diffXv),-gMin(diffXv))*runTime.deltaTValue();

    Info<< "Xv Difference mean: " << dXvAvg << " max: " << dXvNum << endl;
}


// ************************************************************************* //
