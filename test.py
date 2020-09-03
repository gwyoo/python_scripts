#!/usr/bin/python
a = (
	[1, 11, ''],
	[2, 22, ''],
	[3, 33, '']
)

def t1():
	a[0][2] = 'xxx'
	a[1][2] = 'yyy'
	a[2][2] = 'zzz'

def main():
	print a
	t1()
	print a

if __name__ == "__main__":
    main()

	
