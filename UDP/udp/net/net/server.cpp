#include "pch.h"
#include<WinSock2.h>
#include<iostream>
using namespace std;
#pragma comment(lib,"ws2_32.lib")

int main(int argc, char* argv[])
{
	//��ʼ��socket��Դ 
	WSADATA WSAData;
	WORD sockVersion = MAKEWORD(2, 2);
	if (WSAStartup(sockVersion, &WSAData) != 0)
		return 0;

	SOCKET serSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);	//����������socket
	if (INVALID_SOCKET == serSocket)
	{
		cout << "socket error!";
		return 0;
	}

	//���ô���Э�顢�˿��Լ�Ŀ�ĵ�ַ 
	sockaddr_in serAddr;
	serAddr.sin_family = AF_INET;
	serAddr.sin_port = htons(8888);
	serAddr.sin_addr.S_un.S_addr = INADDR_ANY;

	if (bind(serSocket, (sockaddr*)&serAddr, sizeof(serAddr)) == SOCKET_ERROR)	 //��socket�󶨵�ַ 
	{
		cout << "bind error";
		closesocket(serSocket);
		return 0;
	}

	sockaddr_in clientAddr;
	int iAddrlen = sizeof(clientAddr);
	char buff[1024];	//�������ջ����ֽ����� 
	while (true)
	{
		memset(buff, 0, 1024);	//��ս��ջ�������
		//��ʼ�������� 
		int len = recvfrom(serSocket, buff, 1024, 0, (sockaddr*)&clientAddr, &iAddrlen);
		if (len > 0)
		{
			cout << "�ͻ��˵�ַ��" << inet_ntoa(clientAddr.sin_addr) << endl;
			cout << buff;

			//	sendto(serSocket,buff,1024,0,(sockaddr*)&clientAddr,iAddrlen);
		}
	}

	closesocket(serSocket);		//�ر�socket 
	WSACleanup();

	return 0;
}