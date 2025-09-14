void resetArrayToZero(int* arrayPointer, __SIZE_TYPE__ arraySize){
  for(int* endPointer = arrayPointer + arraySize; arrayPointer <= endPointer; ++arrayPointer)
     *arrayPointer = 0;
}

int main2(int size){
  int* array = new int[size];
  resetArrayToZero(array, size);
  return 0;
}