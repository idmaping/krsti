using Aerora.Core;
using Newtonsoft.Json;
using System;
using System.Reflection;

namespace Aerora
{
  
  internal class Program
  {
    
    static void Main(string[] args)
    {

      LeftLegConfig LeftLegConfig = JsonConvert.DeserializeObject<LeftLegConfig>(File.ReadAllText(@".\Config\LeftLeg.json"));
      RightLegConfig RightLegConfig = JsonConvert.DeserializeObject<RightLegConfig>(File.ReadAllText(@".\Config\RightLeg.json"));

      Console.WriteLine(LeftLegConfig);
      Console.WriteLine(RightLegConfig);


    }
  }
}