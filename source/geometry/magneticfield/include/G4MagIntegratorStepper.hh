//
// ********************************************************************
// * DISCLAIMER                                                       *
// *                                                                  *
// * The following disclaimer summarizes all the specific disclaimers *
// * of contributors to this software. The specific disclaimers,which *
// * govern, are listed with their locations in:                      *
// *   http://cern.ch/geant4/license                                  *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.                                                             *
// *                                                                  *
// * This  code  implementation is the  intellectual property  of the *
// * GEANT4 collaboration.                                            *
// * By copying,  distributing  or modifying the Program (or any work *
// * based  on  the Program)  you indicate  your  acceptance of  this *
// * statement, and all its terms.                                    *
// ********************************************************************
//
//
// $Id: G4MagIntegratorStepper.hh,v 1.7 2001/07/11 09:59:09 gunter Exp $
// GEANT4 tag $Name: geant4-04-00 $
//
//
// class G4MagIntegratorStepper
//
// Class description:
//
// Abstract base class for integrator of particle's equation of motion,
// used in tracking in space dependent magnetic field

// History:
// - 15.01.97  J.Apostolakis (J.Apostolakis@cern.ch)

#ifndef G4MAGIntegratorSTEPPER
#define G4MAGIntegratorSTEPPER

#include "globals.hh"
#include "G4EquationOfMotion.hh"

class G4MagIntegratorStepper
{
  public:  // with description

     G4MagIntegratorStepper(G4EquationOfMotion *Equation, G4int num_variables);
     virtual ~G4MagIntegratorStepper();
       // Constructor and destructor. No actions.

     virtual  void  Stepper(  const G4double y[],
			      const G4double dydx[],
			            G4double h,
				    G4double yout[],
				    G4double yerr[]  ) = 0 ;
       // The stepper for the Runge Kutta integration.
       // The stepsize is fixed, with the Step size given by h.
       // Integrates ODE starting values y[0 to 6].
       // Outputs yout[] and its estimated error yerr[].

     virtual  G4double  DistChord() const = 0; 
       // Estimate the maximum distance of a chord from the true path
       // over the segment last integrated.

     inline void NormaliseTangentVector( G4double vec[6] );
       // Simple utility function to (re)normalise 'unit velocity' vector.

     virtual void RightHandSide( const double y[], double dydx[] );   
       // Utility method to supply the standard Evaluation of the
       // Right Hand side of the associated equation.

     inline G4int  GetNumberOfVariables() const;
     inline void   SetNumberOfVariables(G4int newNo);
       // Get/Set the number of variables that the stepper will compile over.

     virtual G4int IntegratorOrder() const = 0;
       // Returns the order of the integrator
       // i.e. its error behaviour is of the order O(h^order).

     inline G4EquationOfMotion *GetEquationOfMotion(); 
       // As some steppers (eg RKG3) require other methods of Eq_Rhs
       // this function allows for access to them.

  public:  // without description

#if 0
     void
     SetChargeAndMomentum( G4double particleCharge, // in e+ units
			   G4double MomentumXc)
       //  Supply the standard Evaluation of the Right Hand side 
       //   of the associated equation.
       {theEquation_Rhs -> SetChargeAndMomentum(particleCharge, MomentumXc);}
#endif 

  private:
  
     G4MagIntegratorStepper(const G4MagIntegratorStepper&);
     G4MagIntegratorStepper& operator=(const G4MagIntegratorStepper&);
       // Private copy constructor and assignment operator.

  private:

     G4EquationOfMotion *fEquation_Rhs;
     G4int              fNumberOfVariables;

};

#include  "G4MagIntegratorStepper.icc"

#endif  /* G4MAGIntegratorSTEPPER */