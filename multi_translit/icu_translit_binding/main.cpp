/********************************************************************
 * COPYRIGHT:
 * Copyright (c) 1999-2002, International Business Machines Corporation and
 * others. All Rights Reserved.
 ********************************************************************/

#include "unicode/translit.h"
#include "unicode/unistr.h"
#include "unicode/ustring.h"
#include "unicode/ustream.h"
#include <stdio.h>
#include <stdlib.h>
#include "UniStrConvert.h"
#include "Translit.h"
// Boost.Python stuff
#include <boost/python.hpp>
using namespace boost::python;
// Define my custom Unicode string type so that it can be 
// easily registered for conversion to a python string later.
using sandbox::MyUniString;



/*
MyUniString GetUniPoints(const UnicodeString &s) {
	int32_t i, length;
	length=s.length();
	char const* ReturnData = "";
	for(i=0; i<1; ++i) {
		//printf(" %04x", s.charAt(i), "\t");
		ReturnData += (" %04x", s.charAt(i));
		//printf(ReturnData, "\n");
	}
	//printf("UniPoints: ", ReturnData, "\t");
	return ReturnData;}
*/

MyUniString GetEngine(int Id) {
	// Parameters sent to the engine need to be UnicodeString
	UnicodeString TransID(Transliterator::getAvailableID(Id));
	//UNICODE_STRING_SIMPLE("English") is deprecated?
	UnicodeString Lang("English");
	UnicodeString TransDispName(Transliterator::getDisplayName(TransID, Lang));
	return TransDispName;
	//return 0;
}

int GetNumberEngines() {
	int TransCount = Transliterator::countAvailableIDs();
	return TransCount;}

UnicodeString ConvertFromHex(char * ConvertThis) {
	// Convert from unicode backslashes to a unicode string
	UErrorCode Status1 = U_ZERO_ERROR;
	//printf("To unicode backslashes\n");
	Transliterator *AnyToHexTrans; //"Latin-Greek"
	AnyToHexTrans = Transliterator::createInstance("Hex-Any", UTRANS_FORWARD, Status1);
    UnicodeString AnyToHexTransUniStr(ConvertThis);
	AnyToHexTrans->transliterate(AnyToHexTransUniStr);
	delete AnyToHexTrans;
	return AnyToHexTransUniStr;}

UnicodeString ConvertToHex(UnicodeString ConvertThis) {
	// Convert to unicode backslashes
	UErrorCode Status3 = U_ZERO_ERROR;
	//printf("Unicode Backslashes\n");
	Transliterator *HexToAnyTrans; //"Latin-Greek"
	HexToAnyTrans = Transliterator::createInstance("Any-Hex", UTRANS_FORWARD, Status3);
	UnicodeString AnyToHexTransUniStr(ConvertThis);
	HexToAnyTrans->transliterate(AnyToHexTransUniStr);
	delete HexToAnyTrans;
	return AnyToHexTransUniStr;}

MyUniString DoTrans(char * TransLitName, char * TransThisStr) {
	UnicodeString AnyToHexTransUniStr;
	AnyToHexTransUniStr = ConvertFromHex(TransThisStr);
	// Create a new transliterator with TransLitName as a parameter and transliterate
	UErrorCode Status2 = U_ZERO_ERROR;
	Transliterator *MyTrans; //"Latin-Greek"
	MyTrans = Transliterator::createInstance(TransLitName, UTRANS_FORWARD, Status2);
	MyTrans->transliterate(AnyToHexTransUniStr);
	AnyToHexTransUniStr = ConvertToHex(AnyToHexTransUniStr);
	// Convert to my custom string type so Boost.Python can properly convert later and return
	MyUniString ReturnData(AnyToHexTransUniStr);
	delete MyTrans;
	return ReturnData;}

BOOST_PYTHON_MODULE(translit) {
	sandbox::init_module();
	def("DoTrans", DoTrans);
	def("GetEngine", GetEngine);
	def("GetNumberEngines", GetNumberEngines);}
