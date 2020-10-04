/*

There is an example of creating one of these here:
https://medium.com/@chris_72272/migrating-to-typescript-write-a-declaration-file-for-a-third-party-npm-module-b1f75808ed2

The basic steps:

1. create a directory like this one, where the declaration files will live
2. add a line to the tsconfig file which points to this directory
3. create specific declaration files, one for each module (<moduleName>/index.d.ts) 
    * these files define 

*/