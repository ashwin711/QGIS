/************************************************************************
 * This file has been generated automatically from                      *
 *                                                                      *
 * src/core/qgsoptionalexpression.h                                     *
 *                                                                      *
 * Do not edit manually ! Edit header and run scripts/sipify.pl again   *
 ************************************************************************/




class QgsOptionalExpression
{
%Docstring

 An expression with an additional enabled flag.

 This can be used for configuration options where an expression can be enabled
 or disabled but when disabled it shouldn't lose it's information for the case
 it gets re-enabled later on and a user shouldn't be force to redo the configuration.

.. versionadded:: 2.18
%End

%TypeHeaderCode
#include "qgsoptionalexpression.h"
%End
  public:

    QgsOptionalExpression();
%Docstring
 Construct a default optional expression.
 It will be disabled and with an empty expression.
%End

    QgsOptionalExpression( const QgsExpression &expression );
%Docstring
 Construct an optional expression with the provided expression.
 It will be enabled.
%End

    QgsOptionalExpression( const QgsExpression &expression, bool enabled );
%Docstring
 Construct an optional expression with the provided expression and enabled state.
%End



    int operator== ( const QgsOptionalExpression &other ) const;
%MethodCode
    sipRes = *sipCpp == *a0;
%End


    int __bool__() const;
%Docstring
 :rtype: int
%End
%MethodCode
    sipRes = sipCpp->enabled();
%End

    bool enabled() const;
%Docstring
 Check if this optional is enabled

.. versionadded:: 3.0
 :rtype: bool
%End

    void setEnabled( bool enabled );
%Docstring
 Set if this optional is enabled

.. versionadded:: 3.0
%End

    QgsExpression data() const;
%Docstring
 Access the payload data

.. versionadded:: 3.0
 :rtype: QgsExpression
%End

    void setData( const QgsExpression &data );
%Docstring
 Set the payload data

.. versionadded:: 3.0
%End

    void writeXml( QDomElement &element );
%Docstring
 Save the optional expression to the provided QDomElement.

 The caller is responsible to pass an empty QDomElement and to append it to
 a parent element.

.. versionadded:: 2.18
%End

    void readXml( const QDomElement &element );
%Docstring
 Read the optional expression from the provided QDomElement.

.. versionadded:: 2.18
%End
};




/************************************************************************
 * This file has been generated automatically from                      *
 *                                                                      *
 * src/core/qgsoptionalexpression.h                                     *
 *                                                                      *
 * Do not edit manually ! Edit header and run scripts/sipify.pl again   *
 ************************************************************************/
