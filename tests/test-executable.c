typedef struct {                                            
  long col1;                                                
  char col2[8];                                             
  long col3;                                                
  char *col4;                                               
} test_struct;                                              

void f1() {}
void f2() {}
void f3() {}

typedef struct {
  long col1;
  void *col2;
  long col3;
  void *col4;
} test_struct_symbols;
                                                            
                                                            
char *test_string = "test_string_value";                    
int test_int = 0xdeadcafe;

int int_array[9] = {10, 20, 30, 40, 50, 60, 70, 80, 90};
                                                            
test_struct test_array[3] = {{0, "value20", 30, "value40"}, 
                             {1, "value21", 31, "value41"}, 
                             {2, "value22", 32, "value42"}};

test_struct_symbols test_array_symbols[3] = {{0, 0, 30, f1},
                                             {1, f2, 31, f3},
                                             {2, f1, 32, f2}};
                                                            
int main() {}
