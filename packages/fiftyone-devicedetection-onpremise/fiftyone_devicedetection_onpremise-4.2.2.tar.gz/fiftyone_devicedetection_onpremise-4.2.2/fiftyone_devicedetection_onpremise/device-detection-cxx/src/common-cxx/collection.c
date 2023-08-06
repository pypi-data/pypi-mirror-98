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

#include "collection.h"
#include "fiftyone.h"

MAP_TYPE(Collection)
#ifndef FIFTYONE_DEGREES_MEMORY_ONLY
MAP_TYPE(CollectionConfig)
#endif

/**
 * Used by methods which retrieve values from a collection to set an exception.
 */
#ifndef FIFTYONE_DEGREES_EXCEPTIONS_DISABLED
#define GET_EXCEPTION_SET(s) \
if (item->data.allocated > 0) { \
	Free(item->data.ptr); \
} \
item->data.ptr = NULL; \
item->data.used = 0; \
item->data.allocated = 0; \
item->handle = NULL; \
item->collection = NULL; \
if (exception->status == NOT_SET) { \
	EXCEPTION_SET(s); \
}
#else
#define GET_EXCEPTION_SET(s)
#endif

 /**
 * Used to work out the number of variable width items can be loaded
 * into a fixed amount of memory.
 */
typedef struct size_counter_t {
	uint32_t count; /* The number of entries read so far */
	uint32_t size; /* The total number of bytes read so far */
	uint32_t max; /* The maximum number of entries to read */
} sizeCounter;

typedef struct in_memory_key_value_t inMemoryKeyValue;

typedef struct in_memory_key_value_t {
	uint32_t key; /* Value of the key */
	void *data; /* Pointer to the data */
	inMemoryKeyValue *next; /* Pointer to the next item or NULL if end */
} inMemoryKeyValue;

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY
bool fiftyoneDegreesCollectionGetIsMemoryOnly() { return false; }
#else
bool fiftyoneDegreesCollectionGetIsMemoryOnly() { return true; }
#endif

/**
 * The following methods are used to release an item when it has been finished
 * with. Each release method differs depending on the implementation of the 
 * collection. For example; releasing an item from a cache collection will 
 * make it eligible for eviction or releasing an item from a file collection
 * will simply free the memory it used.
 */

#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable: 4100) 
#endif
/**
 * Used by memory collection where there is nothing to be done when the release
 * occurs because the memory it uses is only freed when the collection is 
 * freed. 
 */
static void releaseNothing(Item *item) {
	assert(item != NULL);
}
#ifdef _MSC_VER
#pragma warning (default: 4100) 
#pragma warning (pop)
#endif

/**
 * Releases an item held in a cache collection so that it is eligible for 
 * eviction from the cache.
 * @param item to be released and eligible for eviction from the cache. The 
 * handle must reference a cache node.
 */
static void releaseCache(Item *item) {
	if (item->handle != NULL) {
		CacheRelease((CacheNode*)item->handle);
		item->handle = NULL;
	}
}

/**
 * Frees the memory used by the file item and resets the item ready to be used
 * in a subsequent request.
 * @param item to be released with a handle set to the memory to be freed.
 */
static void releaseFile(Item *item) {
	if (item->handle != NULL) {
		Free(item->handle);
		DataReset(&item->data);
		item->handle = NULL;
		item->collection = NULL;
	}
}

/**
 * Calls the collection the item is assigned to's release method. The item may
 * be of any type and must have the collection reference set when it is 
 * initialised.
 * @param item to be released with it's collection reference set.
 */
static void releasePartial(Item *item) {
	if (item->handle != NULL &&
		item->collection != NULL) {
		COLLECTION_RELEASE(item->collection, item);
	}
}

static void freeCollection(Collection *collection) {
	Free(collection->state);
	Free(collection);
}

static void freeMemoryCollection(Collection *collection) {
	CollectionMemory *memory = (CollectionMemory*)collection->state;

	if (collection->next != NULL) {
		collection->next->freeCollection(collection->next);
	}

	if (memory->memoryToFree != NULL) {
		Free(memory->memoryToFree);
	}

	freeCollection(collection);
}

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY

static void freeFileCollection(Collection *collection) {
	freeCollection(collection);
}

static void freeCacheCollection(Collection *collection) {
	Collection *loader;
	CollectionCache *cache = (CollectionCache*)collection->state;
	if (cache->cache != NULL) {

		// Free the loader collection used by the cache.
		loader = (Collection*)cache->cache->loaderState;
		loader->freeCollection(loader);

		// Free the cache itself.
		CacheFree(cache->cache);
	}
	freeCollection(collection);
}

#endif

#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable: 4100) 
#endif
static void* getMemoryVariable(
	Collection *collection,
	uint32_t offset,
	Item *item,
	Exception *exception) {
	CollectionMemory *memory = (CollectionMemory*)collection->state;
	if (offset < collection->size) {
		item->data.ptr = memory->firstByte + offset;
		assert(item->data.ptr < memory->lastByte);
		item->collection = collection;
	}
	else {
		GET_EXCEPTION_SET(COLLECTION_OFFSET_OUT_OF_RANGE);
	}
	return item->data.ptr;
}

static void* getMemoryFixed(
	Collection *collection,
	uint32_t index,
	Item *item,
	Exception *exception) {
	CollectionMemory *memory = (CollectionMemory*)collection->state;
	if (index < collection->count) {
		item->data.ptr = memory->firstByte + ((uint64_t)index * collection->elementSize);
		assert(item->data.ptr < memory->lastByte);
		item->collection = collection;
	}
	else {
		GET_EXCEPTION_SET(COLLECTION_INDEX_OUT_OF_RANGE);
	}
	return item->data.ptr;
}
#ifdef _MSC_VER
#pragma warning (default: 4100) 
#pragma warning (pop)
#endif

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY

static void* getPartialVariable(
	Collection *collection,
	uint32_t offset,
	Item *item,
	Exception *exception) {
	CollectionMemory *memory = (CollectionMemory*)collection->state;
	if (offset < collection->size) {
		item->data.ptr = memory->firstByte + offset;
		assert(item->data.ptr < memory->lastByte);
		item->data.allocated = 0;
		item->data.used = 0;
		item->handle = NULL;
		item->collection = collection;
	}
	else if (collection->next != NULL) {
		collection->next->get(collection->next, offset, item, exception);
	}
	else {
		GET_EXCEPTION_SET(COLLECTION_OFFSET_OUT_OF_RANGE);
	}
	return item->data.ptr;
}

static void* getPartialFixed(
	Collection *collection,
	uint32_t index,
	Item *item,
	Exception *exception) {
	CollectionMemory *memory = (CollectionMemory*)collection->state;
	if (index < collection->count) {
		item->data.ptr = memory->firstByte + ((uint64_t)index * collection->elementSize);
		assert(item->data.ptr < memory->lastByte);
		item->data.allocated = 0;
		item->data.used = collection->elementSize;
		item->handle = NULL;
		item->collection = collection;
	}
	else if (collection->next != NULL) {
		collection->next->get(collection->next, index, item, exception);
	}
	else {
		GET_EXCEPTION_SET(COLLECTION_INDEX_OUT_OF_RANGE);
	}
	return item->data.ptr;
}

static void* getFile(
	Collection *collection,
	uint32_t indexOrOffset,
	Item *item,
	Exception *exception) {
	CollectionFile *file = (CollectionFile*)collection->state;
	void *ptr = NULL;

	// Set the item's handle to the pointer at the start of the data item's
	// data structure following the read operation.
	item->handle = file->read(file, indexOrOffset, &item->data, exception);

	// If the read operation returned a pointer to the item's data then set
	// the collection for the item to the collection used so that it is
	// available when the memory used by the item is released. If the pointer
	// could not be retrieved then set the collection to NULL indicating that
	// no memory free operation is needed.
	if (EXCEPTION_OKAY && item->handle != NULL) {
		item->collection = collection;
		ptr = item->data.ptr;
	}

	return ptr;
}

/**
 * Gets an item from the cache pointed to by the collection's state. If the
 * cache get method returns null or the item fetched is invalid, then the 
 * item's data is unset and null returned.
 * @param collection to use to retrieve the item. Must be of type cache.
 * @param key of the item to be retrieved.
 * @param item data structure to place the value in.
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 * @return a pointer to the data retrieved, or NULL if no data retrieved.
 */
static void* getFromCache(
	Collection *collection,
	uint32_t key,
	Item *item,
	Exception *exception) {
	void *ptr = NULL;
	// Set the collection in the item passed to ensure it can be released when
	// the caller finishes with it.
	item->collection = collection;

	// Get the node from the cache or the loader. This method doesn't need
	// to know which.
	CollectionCache *cache = (CollectionCache*)collection->state;
	CacheNode *node = CacheGet(cache->cache, &key, exception);
	
	if (EXCEPTION_OKAY && node != NULL) {

		// Set the handle in the item passed to ensure  it can be released when
		// the caller finishes with it.
		item->handle = node;

		// If the node was loaded correctly then set the item data to the
		// pointer in the node's data structure.
		if (node->data.ptr != NULL &&
			node->data.used > 0) {
			item->data = node->data;
			ptr = item->data.ptr;
		}
	}
	else {
		item->data.used = 0;
		item->handle = NULL;
	}

	return ptr;
}

/**
 * Loads the data for the key into the data structure passed to the method.
 * @param state information used for the load operation.
 * @param data structure to be used to store the data loaded.
 * @param key for the item in the collection to be loaded.
 * @param exception pointer to an exception data structure to be used if an
 * exception occurs. See exceptions.h.
 */
static void loaderCache(
	const void *state,
	Data *data,
	const void *key,
	Exception *exception) {
	Item item;
	Collection *collection = (Collection*)state;

	// Set the data used to 0 in case the read operation fails for any reason.
	data->used = 0;

	// Get the item from the source collection.
	DataReset(&item.data);
	if (collection->get(
		collection,
		*(uint32_t*)key,
		&item,
		exception) != NULL &&
		EXCEPTION_OKAY) {

		// If the item from the source collection has bytes then copy them into
		// the cache node item ensuring sufficient memory is allocated first.
		if (item.data.used > 0 &&
			DataMalloc(data, item.data.allocated) != NULL) {

			// Copy the data from the collection into the cache.
			if (memcpy(
				data->ptr,
				item.data.ptr,
				item.data.used) == data->ptr) {

				// Set the number of used bytes to match the loaded item.
				data->used = item.data.used;
			}
		}

		// Release the item from the source collection.
		COLLECTION_RELEASE(collection, &item);
	}
}

#endif

static void iterateCollection(
	Collection *collection,
	void *state,
	CollectionIterateMethod callback,
	Exception *exception) {
	Item item;
	uint32_t nextIndexOrOffset = 0;
	DataReset(&item.data);
	while (nextIndexOrOffset < collection->size &&
		collection->get(
			collection,
			nextIndexOrOffset,
			&item,
			exception) != NULL &&
		EXCEPTION_OKAY &&
		// There is valid data for this iteration. Call the callback method.
		callback(state, nextIndexOrOffset, &item.data)) {

		// Set the next index or offset.
		if (collection->elementSize != 0) {
			nextIndexOrOffset++;
		}
		else {
			nextIndexOrOffset += item.data.used;
		}

		// Release the item just retrieved.
		COLLECTION_RELEASE(collection, &item);
	}

	// Release the final item that wasn't released in the while loop.
	// This uses the actual method pointer instead of the macro and is the only
	// place this is necessary. This is the case because even when MEMORY_ONLY
	// is specified, a file collection can still exist internally while
	// creating a memory collection, so the real method must be called here to
	// ensure any allocated memory is freed.
	if (collection->release != NULL) {
		collection->release(&item);
	}
}

#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable: 4100) 
#endif
static bool callbackLoadedSize(
	void *state, 
	uint32_t key, 
	void *data) {
	sizeCounter *tracker = (sizeCounter*)state;
	tracker->size += ((Data*)data)->used;
	tracker->count++;
	return tracker->count < tracker->max;
}
#ifdef _MSC_VER
#pragma warning (default: 4100) 
#pragma warning (pop)
#endif

static sizeCounter calculateLoadedSize(
	Collection *collection,
	const uint32_t count,
	Exception *exception) {
	sizeCounter counter;
	counter.max = count;

	// Can the size be worked out from the element size and the count?
	if (collection->elementSize != 0) {
		counter.count = count > collection->count ? collection->count : count;
		counter.size = counter.count * collection->elementSize;
	}

	// Can the size be worked out from the collection itself?
	else if (collection->size < count) {
		counter.count = 0;
		counter.size = collection->size;
	}

	// If none of the previous options can work then iterate the collection 
	// reading all the values to work out it's size.
	else {
		counter.count = 0;
		counter.size = 0;
		iterateCollection(collection, &counter, callbackLoadedSize, exception);
	}

	return counter;
}

static Collection* createCollection(
	size_t sizeOfState,
	CollectionHeader *header) {
	Collection *collection = (Collection*)Malloc(sizeof(Collection));
	if (collection != NULL) {
		collection->state = Malloc(sizeOfState);
		if (collection->state != NULL) {
			collection->next = NULL;
			collection->elementSize = header->count == 0 ?
				0 : header->length / header->count;
			collection->size = header->length;
			collection->count = header->count;
		}
		else {
			Free(collection);
			collection = NULL;
		}
	}
	return collection;
}

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY

static CollectionFile* readFile(CollectionFile *fileCollection, FILE *file) {
	
	// Set the count of items if not already set and the elements are of a
	// fixed size.
	if (fileCollection->collection->count == 0 &&
		fileCollection->collection->elementSize > 0) {
		fileCollection->collection->count = fileCollection->collection->size /
			fileCollection->collection->elementSize;
	}

	// Record the offset in the source file to the collection.
	fileCollection->offset = ftell(file);

	// Move the file handle past the collection.
	if (fseek(file, fileCollection->collection->size, SEEK_CUR) != 0) {
		return NULL;
	}

	return fileCollection;
}

static Collection* createFromFile(
	FILE *file,
	FilePool *reader,
	CollectionHeader *header,
	CollectionFileRead read) {

	// Allocate the memory for the collection and file implementation.
	Collection *collection = createCollection(
		sizeof(CollectionFile),
		header);
	CollectionFile *fileCollection = (CollectionFile*)collection->state;
	fileCollection->collection = collection;
	fileCollection->reader = reader;

	// Use the read method provided to get records from the file.
	fileCollection->read = read;

	// Read the file data into the structure.
	if (readFile(fileCollection, file) == NULL) {
		freeFileCollection(collection);
		return NULL;
	}

	// Set the get and release functions for the collection.
	collection->get = getFile;
	collection->release = releaseFile;
	collection->freeCollection = freeFileCollection;

	return collection;
}

static Collection* createFromFilePartial(
	FILE *file,
	FilePool *reader,
	CollectionHeader *header,
	int count,
	CollectionFileRead read) {
	EXCEPTION_CREATE;
	sizeCounter counter;

	// Create a file collection to populate the memory collection.
	Collection *source = createFromFile(file, reader, header, read);

	// Allocate the memory for the collection and implementation.
	Collection *collection = createCollection(sizeof(CollectionFile), header);
	CollectionMemory *memory = (CollectionMemory*)collection->state;
	memory->memoryToFree = NULL;
	memory->collection = collection;

	// Get the number of bytes that need to be loaded into memory.
	counter = calculateLoadedSize(source, count, exception);
	if (EXCEPTION_FAILED) {
		freeMemoryCollection(collection);
		source->freeCollection(source);
		return NULL;
	}
	memory->collection->count = counter.count;
	memory->collection->size = counter.size;

	// Allocate sufficient memory for the data to be stored in.
	memory->firstByte = (byte*)Malloc(memory->collection->size);
	if (memory->firstByte == NULL) {
		freeMemoryCollection(collection);
		source->freeCollection(source);
		return NULL;
	}
	memory->memoryToFree = memory->firstByte;

	// Position the file reader at the start of the collection.
	if (fseek(file, header->startPosition, SEEK_SET) != 0) {
		freeMemoryCollection(collection);
		source->freeCollection(source);
		return NULL;
	}

	// Read the portion of the file into memory.
	if (fread(memory->firstByte, 1, memory->collection->size, file) !=
		memory->collection->size) {
		freeMemoryCollection(collection);
		source->freeCollection(source);
		return NULL;
	}

	// Move the file position to the byte after the collection.
	if (fseek(file, source->size - memory->collection->size, SEEK_CUR) != 0) {
		freeMemoryCollection(collection);
		source->freeCollection(source);
		return NULL;
	}

	// Set the last byte to enable checking for invalid requests.
	memory->lastByte = memory->firstByte + memory->collection->size;

	// Set the getter to a method that will check for another collection
	// if the memory collection does not contain the entry.
	if (memory->collection->elementSize != 0) {
		collection->get = getPartialFixed;
	}
	else {
		collection->get = getPartialVariable;
	}
	if (fiftyoneDegreesCollectionGetIsMemoryOnly()) {
		collection->release = NULL;
	}
	else {
		collection->release = releasePartial;
	}
	collection->freeCollection = freeMemoryCollection;

	// Finally free the file collection which is no longer needed.
	source->freeCollection(source);

	return collection;
}

static Collection* createFromFileCached(
	FILE *file,
	FilePool *reader,
	CollectionHeader *header,
	uint32_t capacity,
	uint16_t concurrency,
	CollectionFileRead read) {

	// Allocate the memory for the collection and implementation.
	Collection *collection = createCollection(sizeof(CollectionFile), header);
	CollectionCache *cache = (CollectionCache*)collection->state;
	cache->cache = NULL;

	// Create the file collection to be used with the cache.
	cache->source = createFromFile(file, reader, header, read);
	if (cache->source == NULL) {
		freeCacheCollection(collection);
		return NULL;
	}

	// Create the cache to be used with the collection.
	cache->cache = CacheCreate(
		capacity,
		concurrency,
		loaderCache,
		fiftyoneDegreesCacheHash32,
		cache->source);

	if (cache->cache == NULL) {
		freeCacheCollection(collection);
		return NULL;
	}

	// Copy the source information to the cache collection.
	collection->count = cache->source->count;
	collection->size = cache->source->size;

	// Set the get method for the collection.
	collection->get = getFromCache;
	collection->release = releaseCache;
	collection->freeCollection = freeCacheCollection;

	return collection;
}

/**
 * Either the first collection does not contain any in memory items, or there
 * is a need for a secondary collection to be used if the first does not
 * contain any items. Returns the second collection, or NULL if there is no
 * need for one.
 */
static Collection* createFromFileSecond(
	FILE *file,
	FilePool *reader,
	const CollectionConfig *config,
	CollectionHeader header,
	CollectionFileRead read) {

	// Return the file position to the start of the collection ready to
	// read the next collection.
	if (fseek(file, header.startPosition, SEEK_SET) == 0) {

		// Choose between the cached or file based collection.
		if (config->capacity > 0 && config->concurrency > 0) {

			// If the collection should have a cache then set the next 
			// collection to be cache based.
			return createFromFileCached(
				file,
				reader,
				&header,
				config->capacity,
				config->concurrency,
				read);
		}
		else {

			// If there is no cache then the entries will be fetched 
			// directly from the source file.
			return createFromFile(file, reader, &header, read);
		}
	}

	return NULL;
}

#endif

fiftyoneDegreesCollectionHeader fiftyoneDegreesCollectionHeaderFromMemory(
	fiftyoneDegreesMemoryReader *reader,
	uint32_t elementSize,
	bool isCount) {
	CollectionHeader header;
	if (isCount) {
		// The next integer is the count of items in the data structure.
		header.count = *(uint32_t*)reader->current;
		header.length = header.count * elementSize;
	}
	else {
		// The next integer is the size of the data structure.
		header.length = *(const uint32_t*)reader->current;
		header.count = elementSize > 0 ? header.length / elementSize : 0;
	}

	// Advance the memory reader and record the start of the collection.
	if (MemoryAdvance(reader, sizeof(uint32_t))) {
		header.startPosition = (uint32_t)(reader->current - reader->startByte);
	}
	else {
		header.startPosition = 0;
	}
	
	return header;
}

fiftyoneDegreesCollection* fiftyoneDegreesCollectionCreateFromMemory(
	fiftyoneDegreesMemoryReader *reader,
	fiftyoneDegreesCollectionHeader header) {

	// Validate the header and the reader are in sync at the correct position.
	if ((uint32_t)(reader->current - reader->startByte) !=
		header.startPosition) {
		return NULL;
	}

	// Allocate the memory for the collection and implementation.
	Collection *collection = createCollection(
		sizeof(CollectionMemory),
		&header);
	CollectionMemory *memory = (CollectionMemory*)collection->state;

	// Configure the fields for the collection.
	memory->collection = collection;
	memory->memoryToFree = NULL;
	memory->collection->elementSize = header.count == 0 ? 
		0 : header.length / header.count;
	memory->firstByte = reader->current;
	memory->lastByte = memory->firstByte + memory->collection->size;

	// Assign the get and release functions for the collection.
	if (memory->collection->elementSize != 0) {
		collection->get = getMemoryFixed;
		memory->collection->count = memory->collection->size /
			memory->collection->elementSize;
	}
	else {
		collection->get = getMemoryVariable;
	}
	if (fiftyoneDegreesCollectionGetIsMemoryOnly()) {
		collection->release = NULL;
	}
	else {
		collection->release = releaseNothing;
	}
	collection->freeCollection = freeMemoryCollection;

	// Move over the structure and the size integer checking the move 
	// operation was successful.
	if (MemoryAdvance(
		reader,
		memory->collection->size) == false) {
		collection->freeCollection(collection);
		collection = NULL;
	}

	return collection;
}

fiftyoneDegreesCollectionHeader fiftyoneDegreesCollectionHeaderFromFile(
	FILE *file,
	uint32_t elementSize,
	bool isCount) {
	fiftyoneDegreesCollectionHeader header;
	uint32_t sizeOrCount;

	// Get the size or count of the data structure in bytes.
	if (fread((void*)&sizeOrCount, sizeof(uint32_t), 1, file) == 1) {
		if (isCount) {
			// The integer is the count of items in the data structure.
			header.count = sizeOrCount;
			header.length = header.count * elementSize;
		}
		else {
			// The integer is the size of the data structure.
			header.length = sizeOrCount;
			header.count = elementSize > 0 ? header.length / elementSize : 0;
		}
		header.startPosition = ftell(file);
	}
	else {
		header.startPosition = 0;
	}

	return header;
}

#if defined(_MSC_VER) && defined(FIFTYONE_DEGREES_MEMORY_ONLY)
#pragma warning (disable: 4100)
#endif
fiftyoneDegreesCollection* fiftyoneDegreesCollectionCreateFromFile(
	FILE *file,
	fiftyoneDegreesFilePool *reader,
	const fiftyoneDegreesCollectionConfig *config,
	fiftyoneDegreesCollectionHeader header,
	fiftyoneDegreesCollectionFileRead read) {
	Collection *result = NULL;

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY

	Collection **next = &result;

	if (config->loaded > 0) {

		// If the collection should be partially loaded into memory set the
		// first collection to be a memory collection with the relevant number
		// of entries loaded.
		result = createFromFilePartial(
			file,
			reader,
			&header,
			config->loaded,
			read);

		if (result == NULL) {
			// The collection could not be created from file.
			return NULL;
		
		}
		// Point to the next collection to create.
		next = &result->next;
	}

	if (result == NULL || (
		result->count == config->loaded &&
		(long)result->size < (long)(ftell(file) - header.startPosition))) {

		// Create the next collection if one is needed.
		*next = createFromFileSecond(file, reader, config, header, read);

		if (*next == NULL) {
			// If the secondary collection could not be generated then free
			// the primary one and return NULL to indicate that the collection
			// could not be created.
			if (result != NULL) {
				 result->freeCollection(result);
			}
			result = NULL;
		}
	}
	else {

		// The partial collection supports all items so no need for secondary
		// collections.
		*next = NULL;
	}

#else

	byte *data = (byte*)Malloc(header.length * sizeof(byte));
	MemoryReader memory;

	memory.current = data;
	if (memory.current == NULL) {
		Free(data);
		return NULL;
	}
	
	memory.startByte = memory.current;
	memory.length = (long)header.length;
	memory.lastByte = memory.current + memory.length;

	// Position the file reader at the start of the collection.
	if (fseek(file, header.startPosition, SEEK_SET) != 0) {
		free(data);
		return NULL;
	}

	// Read the portion of the file into memory.
	if (fread(memory.startByte, 1, header.length, file) != header.length) {
		free(data);
		return NULL;
	}

	header.startPosition = 0;
	result = CollectionCreateFromMemory(&memory, header);

	if (result == NULL) {
		free(data);
		return NULL;
	}

	((CollectionMemory*)result->state)->memoryToFree = data;

#endif

	return result;
}
#if defined(_MSC_VER) && defined(FIFTYONE_DEGREES_MEMORY_ONLY)
#pragma warning (default: 4100)
#endif

fiftyoneDegreesFileHandle* fiftyoneDegreesCollectionReadFilePosition(
	const fiftyoneDegreesCollectionFile *file,
	uint32_t offset,
	fiftyoneDegreesException *exception) {
	FileHandle *handle = NULL;

	// If the offset is outside the size of the collection then return NULL.
	if (offset < file->collection->size) {

		// Get the next free handle from the list of readers.
		handle = FileHandleGet(file->reader, exception);

		// The concurrency setting does not allow for another file handle, so 
		// return NULL.
		if (handle != NULL && EXCEPTION_OKAY) {

			// Move to the start of the record in the file handling success or 
			// failure of the operation via the status code.
			if (fseek(handle->file, file->offset + offset, SEEK_SET) != 0) {

				// Release the handle as the operation failed.
				FileHandleRelease(handle);
				EXCEPTION_SET(COLLECTION_FILE_SEEK_FAIL);
				handle = NULL;
			}
		}
	}
	else {
		EXCEPTION_SET(COLLECTION_OFFSET_OUT_OF_RANGE);
	}

	return handle;
}

void* fiftyoneDegreesCollectionReadFileFixed(
	const fiftyoneDegreesCollectionFile *file,
	uint32_t index,
	fiftyoneDegreesData *data,
	fiftyoneDegreesException *exception) {
	void *ptr = NULL;
	FileHandle *handle = NULL;
	uint32_t offset = index * file->collection->elementSize;
	
	// Indicate that no data is being used at the start of the operation.
	data->used = 0;

	// If the index is outside the range of the collection then return NULL.
	if (index < file->collection->count) {

		// Get the handle positioned at the start of the item to be read.
		handle = CollectionReadFilePosition(file, offset, exception);
		if (handle != NULL && EXCEPTION_OKAY) {

			// Ensure sufficient memory is allocated for the item being read.
			if (DataMalloc(data, file->collection->elementSize) != NULL) {

				// Read the record from file to the cache node's data field.
				if (fread(
					data->ptr,
					file->collection->elementSize,
					1,
					handle->file) == 1) {

					// Set the data structure to indicate a successful read.
					data->used = file->collection->elementSize;
					ptr = data->ptr;
				}
				else {

					// The read failed so free the memory allocated and set the
					// status code.
					Free(data->ptr);
					EXCEPTION_SET(COLLECTION_FILE_READ_FAIL);
				}
			}
			else {
				EXCEPTION_SET(INSUFFICIENT_MEMORY);
			}

			// Release the file handle.
			FileHandleRelease(handle);
		}
	}
	else {
		EXCEPTION_SET(COLLECTION_INDEX_OUT_OF_RANGE);
	}

	return ptr;
}

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY

static void* readFileVariable(
	const fiftyoneDegreesCollectionFile *fileCollection,
	FileHandle *handle,
	fiftyoneDegreesData *data,
	uint32_t offset,
	void *initial,
	size_t initialSize,
	fiftyoneDegreesCollectionGetFileVariableSizeMethod getFinalSize,
	Exception *exception) {
	uint32_t bytesNeeded, leftToRead;
	void *ptr = NULL;

	// Set the file position to the start of the item being read.
	if (fseek(handle->file, fileCollection->offset + offset, SEEK_SET) == 0) {

		// Read the item header minus the last part of the structure 
		// that may not always be included with every item.
		if (fread(initial, initialSize, 1, handle->file) == 1) {

			// Calculate the number of bytes needed to store the item.
			bytesNeeded = getFinalSize(initial);

			// Ensure sufficient memory is allocated for the item being
			// read and that the header is copied to the data buffer
			// provided by the caller.
			if (DataMalloc(data, bytesNeeded) != NULL &&
				memcpy(data->ptr, initial, initialSize) == data->ptr) {

				// Read the rest of the item into the item's data 
				// field checking that the whole item was read.
				leftToRead = bytesNeeded - (uint32_t)initialSize;
				if (leftToRead > 0) {
					if (fread(data->ptr + initialSize,
						leftToRead,
						1,
						handle->file) == 1) {

						// The whole item is in the data structure. Set the
						// bytes used and the pointer to be returned.
						data->used = bytesNeeded;
						ptr = data->ptr;
					}
					else {
						Free(data->ptr);
						EXCEPTION_SET(COLLECTION_FILE_READ_FAIL);
					}
				}
				else {

					// The whole item is already in the data structure. Set the
					// bytes used and the pointer to be returned.
					data->used = bytesNeeded;
					ptr = data->ptr;
				}
			}
			else {
				EXCEPTION_SET(INSUFFICIENT_MEMORY);
			}
		}
		else {
			EXCEPTION_SET(COLLECTION_FILE_READ_FAIL);
		}
	}
	else {
		EXCEPTION_SET(COLLECTION_FILE_SEEK_FAIL);
	}

	return ptr;
}

#endif

#if defined(_MSC_VER) && defined(FIFTYONE_DEGREES_MEMORY_ONLY)
#pragma warning (disable: 4100)
#endif
void* fiftyoneDegreesCollectionReadFileVariable(
	const fiftyoneDegreesCollectionFile *fileCollection,
	fiftyoneDegreesData *data,
	uint32_t offset,
	void *initial,
	size_t initialSize,
	fiftyoneDegreesCollectionGetFileVariableSizeMethod getFinalSize,
	fiftyoneDegreesException *exception) {
	void *ptr = NULL;

#ifndef FIFTYONE_DEGREES_MEMORY_ONLY

	fiftyoneDegreesFileHandle *handle = NULL;

	// Indicate that no data is being used at the start of the operation.
	data->used = 0;

	// Check that the item offset is within the range available.
	if (offset < fileCollection->collection->size) {

		// Get the handle for the file operation.
		handle = FileHandleGet(fileCollection->reader, exception);

		// Check the handle is valid. If so then read the variable size data 
		// item.
		if (handle != NULL && EXCEPTION_OKAY) {

			ptr = readFileVariable(
				fileCollection,
				handle,
				data, 
				offset,
				initial, 
				initialSize,
				getFinalSize,
				exception);
			FileHandleRelease(handle);
		}
	}
	else {
		EXCEPTION_SET(COLLECTION_OFFSET_OUT_OF_RANGE);
	}

#endif

	return ptr;
}
#if defined(_MSC_VER) && defined(FIFTYONE_DEGREES_MEMORY_ONLY)
#pragma warning (default: 4100)
#endif

int32_t fiftyoneDegreesCollectionGetInteger32(
	fiftyoneDegreesCollection *collection,
	uint32_t indexOrOffset,
	fiftyoneDegreesException *exception) {
	Item item;
	int32_t value = 0;
	DataReset(&item.data);
	if (collection->get(collection, indexOrOffset, &item, exception) != NULL) {
		value = *((int32_t*)item.data.ptr);
		COLLECTION_RELEASE(collection, &item);
	}
	return value;
}

long fiftyoneDegreesCollectionBinarySearch(
	fiftyoneDegreesCollection *collection,
	fiftyoneDegreesCollectionItem *item,
	uint32_t lowerIndex,
	uint32_t upperIndex,
	void *state,
	fiftyoneDegreesCollectionItemComparer comparer,
	fiftyoneDegreesException *exception) {
	long upper = upperIndex,
		lower = lowerIndex,
		middle;
	int comparisonResult;
	DataReset(&item->data);
	while (lower <= upper) {

		// Get the middle index for the next item to be compared.
		middle = lower + (upper - lower) / 2;

		// Get the item from the collection checking for NULL or an error.
		if (collection->get(collection, middle, item, exception) == NULL ||
			EXCEPTION_OKAY == false) {
			return 0;
		}
		
		// Perform the binary search using the comparer provided with the item
		// just returned.
		comparisonResult = comparer(state, item, middle, exception);
		if (EXCEPTION_OKAY == false) {
			return 0;
		}

		if (comparisonResult == 0) {
			return middle;
		}
		else if (comparisonResult > 0) {
			upper = middle - 1;
		}
		else {
			lower = middle + 1;
		}

		COLLECTION_RELEASE(collection, item);
	}

	// The item could not be found and no error occurred.
	return -1;
}

uint32_t fiftyoneDegreesCollectionGetCount(
	fiftyoneDegreesCollection *collection) {
	while (collection->next != NULL) {
		collection = collection->next;
	}
	return collection->count;
}