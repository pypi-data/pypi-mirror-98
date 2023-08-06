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

#ifndef FIFTYONE_DEGREES_PROPERTY_H_INCLUDED
#define FIFTYONE_DEGREES_PROPERTY_H_INCLUDED

/**
 * @ingroup FiftyOneDegreesCommon
 * @defgroup FiftyOneDegreesProperty Property
 *
 * Property in a data set relating to a single component.
 *
 * ## Introduction
 *
 * A property is stored in a properties collection and contains the meta data
 * for a specific property in a data set.
 *
 * ## Get
 *
 * A property can be fetched from a properties collection in one of two ways:
 *
 * **By Index** : The #fiftyoneDegreesPropertyGet method return the property at
 * a specified index. This provides a way to access a property at a known
 * index, or iterate over all properties.
 *
 * **By Name** : If the index of a property is not known, then the property can
 * be fetched using the #fiftyoneDegreesPropertyGetByName method to find the
 * property in a properties collection.
 *
 * @{
 */

#include <stdint.h>
#ifdef _MSC_VER
#include <windows.h>
#endif
#include "data.h"
#include "exceptions.h"
#include "collection.h"
#include "string.h"

#ifdef __cplusplus
#define EXTERNAL extern "C"
#else
#define EXTERNAL
#endif

/**
 * Enum of property types.
 */
typedef enum e_fiftyone_degrees_property_value_type {
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_STRING = 0, /**< String */
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_INTEGER = 1, /**< Integer */
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_DOUBLE = 2, /**< Double */
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_BOOLEAN = 3, /**< Boolean */
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_JAVASCRIPT = 4, /**< JavaScript string */
	FIFTYONE_DEGREES_PROPERTY_VALUE_SINGLE_PRECISION_FLOAT = 5, /**< Single precision floating point value */
	FIFTYONE_DEGREES_PROPERTY_VALUE_SINGLE_BYTE = 6, /**< Single byte value */
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_COORDINATE = 7, /**< Coordinate */
	FIFTYONE_DEGREES_PROPERTY_VALUE_TYPE_IP_ADDRESS = 8 /**< Ip Range */
} fiftyoneDegreesPropertyValueType;

/**
 * Property structure containing all the meta data relating to a property.
 */
#pragma pack(push, 1)
typedef struct property_t {
	const byte componentIndex; /**< Index of the component */
	const byte displayOrder; /**< The order the property should be displayed in 
	                             relative to other properties */
	const byte isMandatory; /**< True if the property is mandatory and must be
	                            provided */
	const byte isList; /**< True if the property is a list can return multiple 
	                       values */
	const byte showValues; /**< True if the values should be shown in GUIs */
	const byte isObsolete; /**< True if the property is obsolete and will be 
	                           removed from future data sets */
	const byte show; /**< True if the property should be shown in GUIs */
	const byte valueType; /**< The type of value the property represents */
	const uint32_t defaultValueIndex; /**< The default value index for the
	                                     property */
	const uint32_t nameOffset; /**< The offset in the strings structure to the 
	                               property name */
	const uint32_t descriptionOffset; /**< The offset in the strings structure
	                                      to the property description */
	const uint32_t categoryOffset; /**< The offset in the strings structure to
	                                   the property category */
	const uint32_t urlOffset; /**< The offset in the strings structure to the
	                              property URL */
	const uint32_t firstValueIndex; /**< Index of the first possible value */
	const uint32_t lastValueIndex; /**< Index of the last possible value */
	const uint32_t mapCount; /**< Number of maps the property is associated with */
	const uint32_t firstMapIndex; /**< The first index in the list of maps the
	                                  property is associated with */
} fiftyoneDegreesProperty;
#pragma pack(pop)

/**
 * Returns the string name of the property using the item provided. The 
 * collection item must be released when the caller is finished with the
 * string.
 * @param stringsCollection collection of strings retrieved by offsets.
 * @param property structure for the name required.
 * @param item used to store the resulting string in.
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return a pointer to a string in the collection item data structure.
 */
EXTERNAL fiftyoneDegreesString* fiftyoneDegreesPropertyGetName(
	fiftyoneDegreesCollection *stringsCollection,
	fiftyoneDegreesProperty *property,
	fiftyoneDegreesCollectionItem *item,
	fiftyoneDegreesException *exception);

/**
 * Returns the string description of the property using the item provided. The
 * collection item must be released when the caller is finished with the
 * string.
 * @param stringsCollection collection of strings retrieved by offsets.
 * @param property structure for the description required.
 * @param item used to store the resulting string in.
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return a pointer to a string in the collection item data structure.
 */
EXTERNAL fiftyoneDegreesString* fiftyoneDegreesPropertyGetDescription(
	fiftyoneDegreesCollection *stringsCollection,
	fiftyoneDegreesProperty *property,
	fiftyoneDegreesCollectionItem *item,
	fiftyoneDegreesException *exception);

/**
 * Returns the string category of the property using the item provided. The
 * collection item must be released when the caller is finished with the
 * string.
 * @param stringsCollection collection of strings retrieved by offsets.
 * @param property structure for the category required.
 * @param item used to store the resulting string in.
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return a pointer to a string in the collection item data structure.
 */
EXTERNAL fiftyoneDegreesString* fiftyoneDegreesPropertyGetCategory(
	fiftyoneDegreesCollection *stringsCollection,
	fiftyoneDegreesProperty *property,
	fiftyoneDegreesCollectionItem *item,
	fiftyoneDegreesException *exception);

/**
 * Returns the string URL of the property using the item provided. The
 * collection item must be released when the caller is finished with the
 * string.
 * @param stringsCollection collection of strings retrieved by offsets.
 * @param property structure for the URL required.
 * @param item used to store the resulting string in.
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return a pointer to a string in the collection item data structure.
 */
EXTERNAL fiftyoneDegreesString* fiftyoneDegreesPropertyGetUrl(
	fiftyoneDegreesCollection *stringsCollection,
	fiftyoneDegreesProperty *property,
	fiftyoneDegreesCollectionItem *item,
	fiftyoneDegreesException *exception);

/**
 * Gets the value type for the property at the index in the collection.
 * @param properties collection to retrieve the property type from
 * @param index of the property in the collection
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return the value type as a byte for the property at the index.
 */
EXTERNAL byte fiftyoneDegreesPropertyGetValueType(
	fiftyoneDegreesCollection *properties,
	uint32_t index,
	fiftyoneDegreesException *exception);

/**
 * Gets the property at the requested index from the properties collection
 * provided.
 * @param properties to get the property from
 * @param index of the property to get
 * @param item to store the property item in
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return the property requested or NULL
 */
EXTERNAL fiftyoneDegreesProperty* fiftyoneDegreesPropertyGet(
	fiftyoneDegreesCollection *properties,
	uint32_t index,
	fiftyoneDegreesCollectionItem *item,
	fiftyoneDegreesException *exception);

/**
 * Gets the property with the requested name from the properties collection
 * provided.
 * @param properties to get the property from
 * @param strings collection containing the names of the properties
 * @param requiredPropertyName name of the property to get
 * @param item to store the property item in
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return the property requested or NULL
 */
EXTERNAL fiftyoneDegreesProperty* fiftyoneDegreesPropertyGetByName(
	fiftyoneDegreesCollection *properties,
	fiftyoneDegreesCollection *strings,
	const char *requiredPropertyName,
	fiftyoneDegreesCollectionItem *item,
	fiftyoneDegreesException *exception);

/** 
 * @}
 */

#endif