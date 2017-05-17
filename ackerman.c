#include <stdio.h>

//Ackerman recursive fuckitude function
//roop 20170518
//With arguments 4,1 this may take a couple of minutes, result is 65533.
//With arguments 4,2 this will not complete for many billions of years.
//I get a segmentation fault, likely due to repeating stack frames chewing up memory.
//It could be improved by forcing the ack() function to be tail call optimized. 

int ack(int m, int n){
	if(m==0) return n + 1;
	else if (n==0) return ack(m - 1, 1);
	else return ack(m - 1, ack(m, n - 1));
}

int main(){
for(int i = 0; i < 5; i++){
	for(int j = 0; j < 5; j++){
		printf("Ackerman(%i,%i) = ", i, j);
		printf("%i\n", ack(i,j));
	}
}
return 0;
}

