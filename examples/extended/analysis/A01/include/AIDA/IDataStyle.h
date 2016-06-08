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
// -*- C++ -*-
// AID-GENERATED
// =========================================================================
// This class was generated by AID - Abstract Interface Definition          
// DO NOT MODIFY, but use the org.freehep.aid.Aid utility to regenerate it. 
// =========================================================================
#ifndef AIDA_IDATASTYLE_H
#define AIDA_IDATASTYLE_H 1

//  This file is part of the AIDA library
//  Copyright (C) 2002 by the AIDA team.  All rights reserved.
//  This library is free software and under the terms of the
//  GNU Library General Public License described in the LGPL.txt 

#include "AIDA/IBaseStyle.h"

namespace AIDA {

class IFillStyle;
class ILineStyle;
class IMarkerStyle;

/**
 * Style for the part of the scene representing the data
 * (then histograms, functions, data point sets).
 *
 * @author The AIDA team (http://aida.freehep.org/)
 *
 */

class IDataStyle : virtual public IBaseStyle {

public: 
    /// Destructor.
    virtual ~IDataStyle() { /* nop */; }

  /**
   * Return various styles that may be used to 
   * customize the data representation.
   */
    virtual ILineStyle & lineStyle() = 0;

    virtual IMarkerStyle & markerStyle() = 0;

    virtual IFillStyle & fillStyle() = 0;

  /**
   * Set various basic style on the data style.
   */
    virtual bool setLineStyle(const ILineStyle & lineStyle) = 0;

    virtual bool setMarkerStyle(const IMarkerStyle & markerStyle) = 0;

    virtual bool setFillStyle(const IFillStyle & fillStyle) = 0;
}; // class
}; // namespace AIDA
#endif /* ifndef AIDA_IDATASTYLE_H */