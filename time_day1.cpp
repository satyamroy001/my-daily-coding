#include<iostream>
#include <ctime>

using namespace std;

int main()
{
  time_t now= time(0);
  tm *mytm= localtime(&now);
  cout<< "year :"<< 1900+mytm ->tm_year<< endl;
  cout<< "month :"<< 1+mytm ->tm_mon<< endl;
  cout<< "day :"<< mytm ->tm_mday<< endl;
  return 0;
}
