/* *********************************************************************
 * This Original Work is copyright of 51 Degrees Mobile Experts Limited.
 * Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 * Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
 *
 * This Original Work is licensed under the European Union Public Licence (EUPL) 
 * v.1.2 and is subject to its terms as set out below.
 *
 * If a copy of the EUPL was not distributed with this file, You can obtain
 * one at https://opensource.org/licenses/EUPL-1.2.
 *
 * The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 * amended by the European Commission) shall be deemed incompatible for
 * the purposes of the Work and the provisions of the compatibility
 * clause in Article 5 of the EUPL shall not apply.
 * 
 * If using the Work as, or as part of, a network application, by 
 * including the attribution notice(s) required under Article 5 of the EUPL
 * in the end user terms of the application under an appropriate heading, 
 * such notice(s) shall fulfill the requirements of that article.
 * ********************************************************************* */

#ifndef FIFTYONE_DEGREES_TESTS_BASE_INCLUDED
#define FIFTYONE_DEGREES_TESTS_BASE_INCLUDED

#include "pch.h"
#ifdef _MSC_FULL_VER
#define _CRTDBG_MAP_ALLOC
#include <cstdlib>
#include <crtdbg.h>
#endif
#include <stdio.h>
#include <iostream>
#include "../Exceptions.hpp"
#include "../memory.h"
#include "../file.h"

#ifdef _DEBUG
#ifdef _MSC_FULL_VER
#define _CRTDBG_MAP_ALLOC
/* Sampled memory states used to check for memory leaks. */
typedef struct memoryStates_t {
	_CrtMemState s1;
	_CrtMemState s2;
} memoryStates;
#endif
#endif

using namespace std;

/**
 * Adds a test to check the value returned by a get method is equal to the
 * expected value.
 * @param c the test class name being tested
 * @param i the instance of the class being tested
 * @param p the name of the property to be returned
 * @param a optionally any attributes to be passed to the get method
 */
#define TEST_PROPERTY_STRING_EQUAL(c,i,p,a,e) \
TEST_F (c, Property##p) { \
	string value = instance->get##p(a); \
	ASSERT_EQ(value, "e") << "Expected '" << expected << \
		"' but returned '" << value << "'"; \
}

 /**
 * Adds a test to check the value returned by a get method is equal to the
 * expected value.
 * @param c the test class name being tested
 * @param i the instance of the class being tested
 * @param p the name of the property to be returned
 * @param a optionally any attributes to be passed to the get method
 */
#define TEST_PROPERTY_EQUAL(c,p,a,e) \
TEST_F (c, Get##p) { \
	ASSERT_EQ(instance->get##p(a), e) << "Expected '" << e << \
		"' but returned '" << instance->get##p(a) << "'"; \
}

 /**
  * Generates a base test class header for the class provided.
  */
#define TEST_CLASS(c,i) \
class c##Test : public Base { \
public: \
	void SetUp() { Base::SetUp(); instance = new FiftyoneDegrees::Common::c(i); }; \
	void TearDown() { delete instance; Base::TearDown(); }; \
	FiftyoneDegrees::Common::c *instance; \
};

/**
 * Base test class used to carry out memory leak checks. All test classes
 * extending this will be subject to checks ensuring that all memory allocated
 * during the test is cleared up. This class also adds the ability to check
 * that the expected amount of memory is allocated by setting the expected
 * allocation.
 */
class Base : public ::testing::Test {
protected:
	virtual void SetUp();
	virtual void TearDown();
	string GetFilePath(string dataFolderName, string fileName);
	void AssertStatus(fiftyoneDegreesStatusCode status, const char *fileName);
	void runThreads(
		int concurrency,
		FIFTYONE_DEGREES_THREAD_ROUTINE runThread);
private:
#ifdef _DEBUG
#ifdef _MSC_FULL_VER
	memoryStates _states;
#endif
#endif
};

#endif