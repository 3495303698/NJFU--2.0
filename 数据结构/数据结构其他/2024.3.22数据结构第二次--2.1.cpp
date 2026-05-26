#include <stdio.h>
#include <stdlib.h>
typedef struct T_Node
{
	int d;
	struct T_Node *next;
} Node,*List;
List intersection(List La,List Lb)
{
	List dummy;
	List tail=dummy;
	dummy->next=NULL;
	while(La!=NULL&&Lb!=NULL)
	{
		if(La->d==Lb->d)
		{
			tail->next=La;
			tail=tail->next;
			La=La->next;
			Lb=Lb->next;
		}
		else if(La->d<Lb->d)
		{
			La=La->next;
		}
		else
		{
			Lb=Lb->next;
		}
	}
	tail->next=NULL;
	return dummy->next;
}
void createlink(List *pla, List *plb)
{
	int i;
	Node *p;

	*pla = (Node *)malloc(sizeof(Node));     //创建头结点
	p = *pla;

	for(i = 1; i <=10;i++)
	{
		p->next = (Node *)malloc(sizeof(Node));		
		p = p->next;
		p->d = i*2;
		p->next = NULL;
	}


	*plb = (Node *)malloc(sizeof(Node));     //创建头结点
	p = *plb;

	for(i = 1; i <= 8;i++)
	{
		p->next = (Node *)malloc(sizeof(Node));		
		p = p->next;
		p->d = i+6;
		p->next = NULL;
	}
}

int main()
{
	int i;

	List la, lb;
	Node *p;

	createlink(&la, &lb);
	intersection (la, lb);
	
	p = la->next;
	while(p!=NULL)
	{
		printf("%4d",p->d);
		p = p->next;
	}
	printf("\n");
}
