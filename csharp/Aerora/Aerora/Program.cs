using Aerora.Core;
using System;
using System.Reflection;
using dynamixel_sdk;
namespace Aerora
{
  
  internal class Program
  {
    
    static void Main(string[] args)
    {
     // XLService xLService= new XLService();
      //XMService xMService = new XMService();

      List<DXLServiceBase> services = new List<DXLServiceBase>();
    //  services.Add(xLService);
     // services.Add(xMService);

      foreach(DXLServiceBase service in services)
      {
        service.Execute();
      }

    }
  }
}