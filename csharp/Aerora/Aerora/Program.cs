using Aerora.Core;
using System;
using System.Reflection;

namespace Aerora
{
  
  internal class Program
  {
    
    static void Main(string[] args)
    {
      Kinematics k = new Kinematics();
      Console.WriteLine(k.CalculateLeftLeg());
    }
  }
}