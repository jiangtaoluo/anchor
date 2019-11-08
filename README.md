
Anchor-SS
===

### Required code library
`charm-crypto`


The installation steps can be found at the following link :  [charm-crypto](https://blog.csdn.net/qq_34823530/article/details/96605662)

### Instructions  
 The **kn** in *ss_xor_encrypt.cc* and *ss_xor_decrypt.cc* is the order of the XOR matrix, that is, the value of **m**. **N** is the number of ones.  
 !!!!!!!!!When you want to change m and the corresponding matrix, you need to replace kn, **a[kn][kn]**  in the two files and the value **m** in the *t.py*.  
 The **a[kn][kn]** matrix in *encrypt.cc* is the inverse of which in the *decrypt.cc*. For the convenience of matrix find, *decrypt.cc*'s decryption matrix is taken from the upper triangular matrix by various column transformation. The determinant of both matrices is 1 or -1, and the decryption matrix has to make sure that a centain columns are all 1. We have built several **a[kn][kn]** matrices for fixed m and N into *encrypt.cc* and *decrypt.cc* for testing purposes.
### Steps  
1. Generate a block of a certain block size that you want to test in the project folder  
`dd if=/dev/zero of=b.txt bs=1M count=50`  
and we set this block named ***b.txt***,blocksize=bs * count.
1. Modify source file  
For different experiment purpose, we can set diffrent m and a[kn][kn].
In the *t.py*, The value **m** can be set in the asterisk part. As the same, the value **kn** which is equal to **m** can be set in the *ss_xor_encrypt.cc* and *ss.xor_decrypt.cc*. In the two files, the **eachLen = block size / m**, and then change the **a[kn][kn]** in the middle part. Note that the dimension of **a[kn][kn]** must be equal to **m**.
1. Algorithm test  
1).Compile cc file  
`./process2.sh`  
2)Perform xor encryption  
`./encrypt.out`  
Record the total encryption time.  
3)Perform xor decryption  
`./decrypt.out`  
Record the total decryption time.  
4)Ramdamly select an anchor, encrypt and decrypt it and then record the time  
`python t.py`  
5)Process the data in the previous step  
`./processall`  

And then you can get the data in the file *Record.out*.

