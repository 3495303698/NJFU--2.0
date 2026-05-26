#include <stdio.h>
#include <stdlib.h>

typedef struct DuLnode
{
    int data;
    struct DuLnode *next, *prior;
}DuLnode, *DuLLinklist;

DuLLinklist CreateDuLlist(DuLLinklist L, int n)
{
    //创建头节点
    L->next = NULL;
    L->prior = NULL;
    //头插法创建双向链表
    //头插法，插入的第一个节点和后续要插入的节点的方式有所不同
    //插入第一个节点不需要考虑后继节点
    //第二个节点开始要考虑后继节点的前驱指针
    for(int i = 0; i < n; i++)
    {
        DuLLinklist newNode = (DuLLinklist)malloc(sizeof(DuLnode));
        printf("请输入要插入的节点值：");
        scanf("%d", &newNode->data);
        if(L->next == NULL)//插入第一个节点时
        {
            L->next = newNode;//头节点的next域指向新插入的节点
            newNode->prior = L;//新插入节点的prior域指向头节点
            newNode->next = NULL;//新插入节点的next赋空
        }
        else//插入后续节点
        {
            newNode->next = L->next;//将上一个插入的节点连接到新插入的节点的next域
            L->next->prior = newNode;//将上一个插入的节点的前驱prior域指向新插入的节点
            newNode->prior = L;//新插入节点的前驱域指向头节点
            L->next = newNode;//头节点的next域指向新插入的节点
        }
    }
}

void Printlist(DuLLinklist L, int n)
{
    DuLLinklist temp = L->next;
    printf("链表为：");
    for(int i = 0; i < n; i++)
    {
        printf("%d ", temp->data);
        temp = temp->next;
    }
}

DuLLinklist Listdelete(DuLLinklist L, int i)
{
    //DuLLinklist s = (DuLLinklist)malloc(sizeof(DuLnode));
    DuLLinklist temp = (DuLLinklist)malloc(sizeof(DuLnode));
    temp = L->next;
    int cnt = 1;
    while(cnt != i)//找到第i个要删除的节点
    {
        temp = temp->next;
        cnt++;
    }
    if(temp->next != NULL)
    {
        int e = temp->data;//保留要删除节点的数据
        temp->prior->next = temp->next;//该删除节点的前驱节点的next域连接到该删除节点的后继节点
        temp->next->prior = temp->prior;//该删除节点的后继节点的prior域连接到该删除节点的前驱节点
        free(temp);
    }
    else//如果删除的是最后一个节点
    {
        temp->prior->next = NULL;
        free(temp);
    }
}
int main()
{
    DuLLinklist L = (DuLLinklist)malloc(sizeof(DuLnode));
    int n, i;
    printf("请输入要创建多少个节点：");
    scanf("%d", &n);
    CreateDuLlist(L, n);
    printf("链表为：");
    Printlist(L, n);
    printf("输入要删除的节点：");
    scanf("%d", &i);
    Listdelete(L, i);
    Printlist(L, n);
    return 0;
}