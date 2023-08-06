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

#ifndef FIFTYONE_DEGREES_EVIDENCE_H_INCLUDED
#define FIFTYONE_DEGREES_EVIDENCE_H_INCLUDED

/**
 * @ingroup FiftyOneDegreesCommon
 * @defgroup FiftyOneDegreesEvidence Evidence
 *
 * Contains key value pairs as evidence to be processed.
 *
 * ## Introduction
 *
 * An Evidence structure contains key value pairs to be parsed and processed
 * by an engine.
 *
 * Items of evidence (e.g. an HTTP header) are added to the structure. The
 * values are then parsed based on the key prefix. In the case of an HTTP
 * header the string would simply be copied, but other types can require
 * further parsing.
 * Evidence items can then be accessed by engines in their parsed form,
 * enabling simpler processing.
 *
 * ## Creation
 *
 * An evidence structure is created using the #fiftyoneDegreesEvidenceCreate
 * method. This takes the maximum number of evidence items which the structure
 * can store.
 *
 * ## Prefixes
 *
 * Evidence keys contain a prefix and the key within that prefix. For example,
 * the key `header.user-agent` has the prefix `header` indicating that the
 * second part of the key is an HTTP header name (`user-agent`).
 *
 * Prefixes are stored as an enum value with the type of
 * #fiftyoneDegreesEvidencePrefix. The enum value of the prefix can be found
 * for a key string by using the #fiftyoneDegreesEvidenceMapPrefix method which
 * takes the key string as an argument, and returns the enum value.
 *
 * Prefix values are defined by their bit positions such that multiple prefixes
 * can be filtered when iterating with the #fiftyoneDegreesEvidenceIterate
 * method. For example, to iterate over all HTTP headers and all query
 * parameters two prefixes can be used in combination like
 * `FIFTYONE_DEGREES_EVIDENCE_HTTP_HEADER_STRING | FIFTYONE_DEGREES_EVIDENCE_QUERY`.
 *
 * ## Add
 *
 * An item of evidence is added to the evidence structure using the
 * #fiftyoneDegreesEvidenceAddString method. This then parses the string value
 * it is provided into the correct type which is determined by the prefix.
 *
 * ## Iterate
 *
 * The evidence a particular evidence structure can be iterated over using the
 * #fiftyoneDegreesEvidenceIterate method. This takes a prefix filter (as
 * described in the Prefixes section above), and a callback method which is
 * called for each evidence item which matches the filter. The number of
 * matching items is then returned.
 *
 * ## Free
 *
 * An evidence structure is freed using the #fiftyoneDegreesEvidenceFree
 * method. It is important to note that this method does **NOT** free the
 * original values which are referenced by the structure.
 *
 * ## Usage Example
 *
 * ```
 * void *state;
 * fiftyoneDegreesEvidenceIterateMethod doSomethingToAValue;
 *
 * // Create an evidence structure large enough to hold a single item of
 * // evidence
 * fiftyoneDegreesEvidenceKeyValuePairArray* evidence =
 *     fiftyoneDegreesEvidenceCreate(1);
 *
 * // Add an item of evidence which is a string
 * fiftyoneDegreesEvidenceAddString(
 *     evidence,
 *     fiftyoneDegreesEvidenceMapPrefix("header"),
 *     "some-header-name",
 *     "some-header-value");
 *
 * // Iterate over all HTTP header evidence and call a method which does
 * // something to each item
 * int numberIterated = fiftyoneDegreesEvidenceIterate(
 *     evidence,
 *     FIFTYONE_DEGREES_EVIDENCE_HTTP_HEADER_STRING,
 *     state,
 *     doSomethingToAValue);
 *
 * // Free the evidence
 * fiftyoneDegreesEvidenceFree(evidence);
 * ```
 *
 * @{
 */

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include "data.h"
#include "ip.h"
#include "string.h"
#include "array.h"

#ifdef __cplusplus
#define EXTERNAL extern "C"
#else
#define EXTERNAL
#endif

/**
 * Evidence prefixes used to determine the category a piece of evidence
 * belongs to. This will determine how the value is parsed.
 */
typedef enum e_fiftyone_degrees_evidence_prefix {
	FIFTYONE_DEGREES_EVIDENCE_HTTP_HEADER_STRING = 1 << 0, /**< An HTTP header
														   value */
	FIFTYONE_DEGREES_EVIDENCE_HTTP_HEADER_IP_ADDRESSES = 1 << 1, /**< A list of
																 IP addresses
																 as a string to
																 be parsed into
																 a IP addresses
																 collection. */
	FIFTYONE_DEGREES_EVIDENCE_SERVER = 1 << 2, /**< A server value e.g. client
											   IP */
	FIFTYONE_DEGREES_EVIDENCE_QUERY = 1 << 3, /**< A query string parameter */
	FIFTYONE_DEGREES_EVIDENCE_COOKIE = 1 << 4, /**< A cookie value */
	FIFTYONE_DEGREES_EVIDENCE_IGNORE = 1 << 7, /**< The evidence is invalid and
											   should be ignored */
} fiftyoneDegreesEvidencePrefix;

/** Map of prefix strings to prefix enum values. */
typedef struct fiftyone_degrees_evidence_prefix_map_t {
	const char *prefix; /**< Name of the prefix */
	size_t prefixLength; /**< Length of the prefix string */
	fiftyoneDegreesEvidencePrefix prefixEnum; /**< Enum value of prefix name */
} fiftyoneDegreesEvidencePrefixMap;

/**
 * Evidence key value pair structure which combines the prefix, key and value.
 */
typedef struct fiftyone_degrees_evidence_key_value_pair_t {
	fiftyoneDegreesEvidencePrefix prefix; /**< e.g. #FIFTYONE_DEGREES_EVIDENCE_HTTP_HEADER_STRING */
	const char *field; /**< e.g. User-Agent or ScreenPixelsWidth */
	const void *originalValue; /**< The original unparsed value */
	const void *parsedValue; /**< The parsed value which may not be a string */
} fiftyoneDegreesEvidenceKeyValuePair;

#define EVIDENCE_KEY_VALUE_MEMBERS \
struct fiftyone_degrees_array_fiftyoneDegreesEvidenceKeyValuePair_t* pseudoEvidence; /**< The pseudo evidence. #fiftyoneDegreesEvidenceKeyValuePairArray type */

FIFTYONE_DEGREES_ARRAY_TYPE(
	fiftyoneDegreesEvidenceKeyValuePair,
	EVIDENCE_KEY_VALUE_MEMBERS)


/**
 * Callback method used to iterate evidence key value pairs.
 * @param state pointer provided to the iterator
 * @param pair evidence key value pair with the parsed value set
 * @return true if the iteration should continue otherwise false
 */
typedef bool(*fiftyoneDegreesEvidenceIterateMethod)(
	void *state, 
	fiftyoneDegreesEvidenceKeyValuePair *pair);

/**
 * Creates a new evidence array with the capacity requested.
 * @param capacity maximum number of evidence items
 * @return pointer to the newly created array
 */
EXTERNAL fiftyoneDegreesEvidenceKeyValuePairArray* 
fiftyoneDegreesEvidenceCreate(uint32_t capacity);

/**
 * Frees the memory used by an evidence array.
 * @param evidence pointer to the array to be freed
 */
EXTERNAL void fiftyoneDegreesEvidenceFree(
	fiftyoneDegreesEvidenceKeyValuePairArray *evidence);

/**
 * Adds a new entry to the evidence. The memory associated with the 
 * field and original value parameters must not be freed until after the 
 * evidence collection has been freed. This method will NOT copy the values.
 * @param evidence pointer to the evidence array to add the entry to
 * @param prefix enum indicating the category the entry belongs to
 * @param field used as the key for the entry within its prefix
 * @param originalValue the value to be parsed
 */
EXTERNAL fiftyoneDegreesEvidenceKeyValuePair* fiftyoneDegreesEvidenceAddString(
	fiftyoneDegreesEvidenceKeyValuePairArray *evidence,
	fiftyoneDegreesEvidencePrefix prefix,
	const char *field,
	const char *originalValue);

/**
 * Determines the evidence map prefix from the key.
 * @param key the evidence key including the evidence prefix .i.e. header
 * @return the prefix enumeration, or NULL if one does not exist
 */
EXTERNAL fiftyoneDegreesEvidencePrefixMap* fiftyoneDegreesEvidenceMapPrefix(
	const char *key);

/**
 * Iterates over the evidence calling the callback method for any values that
 * match the prefixes provided. If there are pseudo evidence, this
 * will also iterate through them and perform the callback on each.
 *
 * @param evidence key value pairs including prefixes
 * @param prefixes one or more prefix flags to return values for
 * @param state pointer passed to the callback method
 * @param callback method called when a matching prefix is found
 * @return the number of matching evidence keys iterated over
 */
EXTERNAL uint32_t fiftyoneDegreesEvidenceIterate(
	fiftyoneDegreesEvidenceKeyValuePairArray *evidence,
	int prefixes,
	void *state,
	fiftyoneDegreesEvidenceIterateMethod callback);

/**
 * @}
 */

#endif