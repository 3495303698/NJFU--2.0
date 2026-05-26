#include <stdio.h>
#include <stdlib.h>
typedef struct T_Node
{
	int d;
	struct T_Node *next;
} Node, *List;
void LinkReverse(List *pla)
{
	List prev=NULL;
	List c=*pla;
	List next=NULL;
	List d=*pla;
	while(c!=NULL)
	{
		next=c->next;
		c->next=prev;
		prev=c;
		c=next;
	}
	d->next=prev;
}
void createlink(List *pla)
{
	int i;
	Node *p;

	*pla = (Node *)malloc(sizeof(Node));     //创建头结点
	p = *pla;

	for(i = 1; i <=10;i++)
	{
		p->next = (Node *)malloc(sizeof(Node));		
		p = p->next;
		p->d = i;
		p->next = NULL;
	}
}


int main( )
{
	List la, p;
	int i;

	createlink(&la);
	LinkReverse(&la);

	p = la->next;
	for(i = 1; i <=10;i++)
	{
		printf("%4d",p->d);
		p = p->next;
	}
	printf("\n");
}