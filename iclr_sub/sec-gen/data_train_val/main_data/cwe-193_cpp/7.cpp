void initializeMemoryManagementUnit(){

	void* allocationContext = allocatePhysicalMemory(1);
	memset(allocationContext, 0, PAGE_SIZE);

	extern volatile struct MemoryMapRequest memoryMapRequest;
	struct MemoryMapEntry **mapEntries = memoryMapRequest.response->entries;
	size_t entriesCount = memoryMapRequest.response->entry_count;

	extern int _codeSegmentStart, _codeSegmentEnd, _readOnlyDataStart, _readOnlyDataEnd, _dataSegmentStart, _dataSegmentEnd;

	void* codeStart = &_codeSegmentStart;
	void* codeEnd   = &_codeSegmentEnd;
	void* readOnlyStart = &_readOnlyDataStart;
	void* readOnlyEnd   = &_readOnlyDataEnd;
	void* dataStart   = &_dataSegmentStart;
	void* dataEnd     = &_dataSegmentEnd;

	printf("CODE START: %p CODE END: %p\nREAD-ONLY DATA START: %p READ-ONLY DATA END: %p\nDATA START: %p DATA END: %p\n", codeStart, codeEnd, readOnlyStart, readOnlyEnd, dataStart, dataEnd);

	if(!kernelAddressRequest.response) _panic("Kernel physical base not passed by bootloader", 0);

	void* kernelPhysicalBase = kernelAddressRequest.response->physical_base;

	printf("Kernel physical base: %p\n", kernelPhysicalBase);

	for(void* address = codeStart; address <= codeEnd; address += PAGE_SIZE){
		uint64_t memoryEntry;
		updateMemoryEntry(&memoryEntry, kernelPhysicalBase, ARCH_MMU_MAP_READ);
		mapPhysicalToVirtual(allocationContext, address, memoryEntry);

		kernelPhysicalBase += PAGE_SIZE;
	}

	switchMemoryContext(allocationContext);
	getCurrentContext()->context->context = allocationContext;

	printf("In bootstrap context\n");

}
