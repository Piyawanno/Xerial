# Environment: Library

| Deployment | Book                                                                                                                       | Librarian                                                          | Library                                                         | 
|------------|----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------------|
| 1          | [0]                                                                                                                        | [0]                                                                | [0]                                                             | 
| 2          | [1] <br/>RENAME title bookTitle                                                                                            | [1] <br/>ADD phoneNumber StringColumn<br/>ADD address StringColumn | [1] <br/>RENAME name libraryName                                |
| 3          | [2] <br/>ADD fee IntegerColumn<br/>ADD totalSales FloatColumn                                                              | [2] <br/>ADD DateOfBirth DateColumn                                | [2] <br/>ADD createDate DateColumn                              |
| 4 [Freeze] | [3] <br/>DROP totalSales FloatColumn<br/>CHANGE_TYPE fee IntegerColumn to FloatColumn<br/>CHANGE_LENGTH bookTitle 10 to 20 | [3] <br/>RENAME DateOfBirth DOB                                    | [2]                                                             |
| 5          | [4] <br/>DROP fee FloatColumn                                                                                              | [3]                                                                | [3] <br/>ADD telephone StringColumn                             |                             
| 6          | [5] <br/>CHECKOUT to 2<br/>SKIP [3] CHANGE_TYPE fee IntegerColumn to FloatColumn                                           | [4] <br/>ADD startWorkingTime TimeColumn                           | [3]                                                             |
| 7          | [6] <br/>CHECKOUT to 0                                                                                                     | [5] <br/>CHECKOUT to 1                                             | [4] <br/>CHECKOUT to 1<br/>SKIP  [3] ADD telephone StringColumn |