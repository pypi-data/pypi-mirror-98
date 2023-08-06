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

#ifndef FIFTYONE_DEGREES_INIT_H_INCLUDED
#define FIFTYONE_DEGREES_INIT_H_INCLUDED

/**
 * @ingroup FiftyOneDegreesCommon
 * @defgroup FiftyOneDegreesStatus Status
 *
 * Status codes and messages indicating the result of an operation.
 *
 * ## Introduction
 *
 * A status code is an enum indicating the result of an operation, usually
 * the initialisation of something. If the status is anything other than
 * #FIFTYONE_DEGREES_STATUS_SUCCESS, then the operation was not successful. In
 * that case, the status code indicates the nature of the failure. 
 *
 * A status code can be returned by any method that wishes to report a specific
 * error rather than just returning `NULL`.
 *
 * Examples of error status codes are `insufficient memory` or `corrupt data`.
 * If an operation was successful then this is reported in the same way by
 * returning a `success` status code.
 *
 * Status codes have related messages which can be fetched using the
 * #fiftyoneDegreesStatusGetMessage method. The messages are intended to be
 * useful messages which are returned to the user in the event of an error
 * occurring.
 *
 * ## Usage Example
 *
 * ```
 * const char *fileName;
 * fiftyoneDegreesStatusCode status;
 *
 * // Check whether the result of an operation was successful
 * if (status != FIFTYONE_DEGREES_STATUS_SUCCESS) {
 *
 *     // Get the status message as the operation has not succeeded
 *     const char *message = fiftyoneDegreesStatusGetMessage(status, fileName);
 *
 *     // Do something with the message
 *     // ...
 * }
 * ```
 *
 * @{
 */

#include <stdint.h>
#include <string.h>
#include <stdio.h>

#ifdef __cplusplus
#define EXTERNAL extern "C"
#else
#define EXTERNAL
#endif

/** Status returned from the initialisation of a resource. */
typedef enum e_fiftyone_degrees_status_code {
	FIFTYONE_DEGREES_STATUS_SUCCESS, /**< All okay */
	FIFTYONE_DEGREES_STATUS_INSUFFICIENT_MEMORY, /**< Lack of memory */
	FIFTYONE_DEGREES_STATUS_CORRUPT_DATA, /**< Data structure not readable */
	FIFTYONE_DEGREES_STATUS_INCORRECT_VERSION, /**< Data not the required
											   version */
	FIFTYONE_DEGREES_STATUS_FILE_NOT_FOUND, /**< The data file couldn't be
											found */
	FIFTYONE_DEGREES_STATUS_FILE_BUSY, /**< The data file was busy */
	FIFTYONE_DEGREES_STATUS_FILE_FAILURE, /**< Unknown file error */
	FIFTYONE_DEGREES_STATUS_NOT_SET, /**< Should never be returned to the
									 caller */
	FIFTYONE_DEGREES_STATUS_POINTER_OUT_OF_BOUNDS, /**< Working pointer
												   exceeded the amount of
												   memory containing the data */
	FIFTYONE_DEGREES_STATUS_NULL_POINTER, /**< A key pointer was not set */
	FIFTYONE_DEGREES_STATUS_TOO_MANY_OPEN_FILES, /**< Too many files are open */
	FIFTYONE_DEGREES_STATUS_REQ_PROP_NOT_PRESENT, /**< None of the required
	                                                  properties could be found */
	FIFTYONE_DEGREES_STATUS_PROFILE_EMPTY, /**< The profile id represents an
										   empty profile */
	FIFTYONE_DEGREES_STATUS_COLLECTION_FAILURE, /**< There was an error getting
	                                                an item from a collection
	                                                due to too many concurrent 
	                                                operations */
	FIFTYONE_DEGREES_STATUS_FILE_COPY_ERROR, /**< The data file could not be 
	                                             copied */
	FIFTYONE_DEGREES_STATUS_FILE_EXISTS_ERROR, /**< The file or directory
											   already exists, so could not be
											   created */
	FIFTYONE_DEGREES_STATUS_FILE_WRITE_ERROR, /**< The data file could not be 
	                                              created */
	FIFTYONE_DEGREES_STATUS_FILE_PERMISSION_DENIED, /**< File permission denied */
	FIFTYONE_DEGREES_STATUS_FILE_PATH_TOO_LONG, /**< The file path is longer
	                                                than the available memory
	                                                available to store it */
	FIFTYONE_DEGREES_STATUS_ENCODING_ERROR, /**< There was an error encoding
	                                            characters of a string */
	FIFTYONE_DEGREES_STATUS_INVALID_COLLECTION_CONFIG, /**< The configuration 
	                                                   provided to create a 
	                                                   collection could not be 
	                                                   used to create a valid 
	                                                   collection */
	FIFTYONE_DEGREES_STATUS_INVALID_CONFIG, /**< An invalid config was provided */
	FIFTYONE_DEGREES_STATUS_INSUFFICIENT_HANDLES, /**< There were not enough
	                                                  handles available to
	                                                  retrieve data from the
	                                                  source*/
	FIFTYONE_DEGREES_STATUS_COLLECTION_INDEX_OUT_OF_RANGE, /**< Index out of
														   range */
	FIFTYONE_DEGREES_STATUS_COLLECTION_OFFSET_OUT_OF_RANGE, /**< Offset out of
															range */
	FIFTYONE_DEGREES_STATUS_COLLECTION_FILE_SEEK_FAIL, /**< Seek failure */
	FIFTYONE_DEGREES_STATUS_COLLECTION_FILE_READ_FAIL, /**< Read failure */
	FIFTYONE_DEGREES_STATUS_INCORRECT_IP_ADDRESS_FORMAT /**< IP address 
														format is incorrect */
} fiftyoneDegreesStatusCode;

/**
 * Returns an English error message for the status code allocating memory 
 * needed to store the message. The caller must free the memory when they have 
 * finished consuming the error message.
 * @param status code to get the message for
 * @param fileName the source file used for initialisation, or NULL if not
 * applicable to the status code
 * @return pointer to the newly allocated message string
 */
EXTERNAL const char* fiftyoneDegreesStatusGetMessage(
	fiftyoneDegreesStatusCode status,
	const char *fileName);

/**
 * @}
 */

#endif