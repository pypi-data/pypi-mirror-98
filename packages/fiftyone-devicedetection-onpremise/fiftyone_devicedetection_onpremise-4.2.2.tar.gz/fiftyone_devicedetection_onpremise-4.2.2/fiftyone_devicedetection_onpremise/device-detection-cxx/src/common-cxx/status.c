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

#include "status.h"

#include "fiftyone.h"

typedef struct fiftyone_degrees_status_message {
	StatusCode status;
	const char *message;
} StatusMessage;

static StatusMessage messages[] = {
	{ SUCCESS,
		"The operation was successful."},
	{ INSUFFICIENT_MEMORY, 
		"Insufficient memory allocated for the operation." },
	{ CORRUPT_DATA,
		"The data was not in the correct format. Check the data file is "
		"uncompressed." },
	{ INCORRECT_VERSION,
		"The data is an unsupported version. Check you have the latest data "
		"and API." },
	{ FILE_NOT_FOUND,
		"The data file '%s' could not be found. Check the file path and that "
		"the program has sufficient read permissions." },
	{ FILE_FAILURE,
		"An unknown error occurred accessing the file '%s'. Check the file "
		"path and that the program has sufficient read permissions." },
	{ NULL_POINTER,
		"Null pointer to the existing dataset or memory location." },
	{ POINTER_OUT_OF_BOUNDS,
		"Allocated continuous memory containing 51Degrees data file appears "
		"to be smaller than expected. Most likely because the data file was "
		"not fully loaded into the allocated memory." },
	{ TOO_MANY_OPEN_FILES,
		"Too many file handles have been created during initialisation."},
	{ REQ_PROP_NOT_PRESENT,
		"None of the properties requested could be found in the data file, so "
		"no properties can be initialised. To initialise all available "
		"properties, set the field to null." },
	{ PROFILE_EMPTY,
		"The profile id related to an empty profile. As this just represents "
		"an empty profile, there is no profile which can be returned." },
	{ COLLECTION_FAILURE,
		"There was an error getting an item from a collection within the "
		"data set. This is likely to be caused by too many concurrent "
		"operations. Increase the concurrency option in the collection "
		"configuration to allow more threads to access the collection "
		"simultaneously." },
	{ FILE_COPY_ERROR,
		"There was an error copying the source file to the destination. "
		"Verify sufficient space is available at the destination." },
	{ FILE_EXISTS_ERROR,
		"The file or directory already exists so could not be created." },
	{ FILE_WRITE_ERROR,
		"Could not create the file with write permissions." },
	{ FILE_PERMISSION_DENIED,
		"Permission denied when opening file." },
	{ FILE_PATH_TOO_LONG,
		"The file path to the data file is longer than the memory available "
		"to store it. Use a shorter data file path." },
	{ ENCODING_ERROR,
		"There was an error encoding characters of the string. Ensure all "
		"characters are valid." },
	{ INVALID_COLLECTION_CONFIG,
		"The configuration provided could not be used to create a valid "
		"collection. If a cached collection is included in the configuration "
		"this maybe caused by insufficient capacity for the concurrency."},
	{ INVALID_CONFIG,
		"The configuration provided was not valid, and has caused a failure "
		"while building the resource it configures." },
	{ INSUFFICIENT_HANDLES,
		"Insufficient handles available in the pool. Verify the pool has " 
		"sufficient handles to support the maximum number of concurrent "
		"threads." },
	{ COLLECTION_INDEX_OUT_OF_RANGE, 
		"Index used to retrieve an item from a collection was out of range." },
	{ COLLECTION_OFFSET_OUT_OF_RANGE, 
		"Offset used to retrieve an item from a collection was out of range." },
	{ COLLECTION_FILE_SEEK_FAIL, 
		"A seek operation on a file failed." },
	{ COLLECTION_FILE_READ_FAIL,
		"A read operation on a file failed." },
	{ INCORRECT_IP_ADDRESS_FORMAT,
		"The input IP address format is incorrect. Verify the input IP address "
		"string has correct format. If passing a byte array, verify the "
		"associated input data is also consistent." }
};

static char defaultMessage[] = "Status code %i does not have any message text.";

const char* fiftyoneDegreesStatusGetMessage(
	fiftyoneDegreesStatusCode status,
	const char *fileName) {
	uint32_t i;
	size_t messageSize;
	StatusMessage *current;
	char *message = NULL;
	if (fileName == NULL) {
		fileName = "null";
	}
	
	for (i = 0; i < sizeof(messages) / sizeof(StatusMessage); i++) {
		current = &messages[i];
		if (current->status == status) {
			messageSize = strstr(current->message, "%s") ?
				// message + dataFile + '\0' - "%s"
				strlen(current->message) + strlen(fileName) - 1 :
				// message + '\0'
				strlen(current->message) + 1;
			message = (char*)Malloc(messageSize);
			if (message != NULL) {
				sprintf(message, current->message, fileName);
			}
			break;
		}
	}
	if( message == NULL) {
		messageSize = sizeof(defaultMessage) + 5;
		message = (char*)Malloc(messageSize);
		sprintf(message, defaultMessage, (int)status);
	}
	return message;
}