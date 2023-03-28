using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace Aerora.Core
{
  public class Kinematics
  {
    LeftLegConfig _LeftLegConfig = JsonConvert.DeserializeObject<LeftLegConfig>(File.ReadAllText(@".\Config\LeftLeg.json"));
    RightLegConfig _RightLegConfig = JsonConvert.DeserializeObject<RightLegConfig>(File.ReadAllText(@".\Config\RightLeg.json"));
    public void Run()
    {
      Console.WriteLine(_LeftLegConfig.Femur);
      Console.WriteLine(_RightLegConfig.Femur);

    }

  }
}
