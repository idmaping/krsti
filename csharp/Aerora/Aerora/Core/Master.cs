using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Aerora.Core
{
  /// <summary>
  /// Segala kebutuhan didalam Core silahkan taruh sini
  /// </summary>
  public class Master
  {
    public LeftLegConfig leftLegConfig;
    public RightLegConfig rightLegConfig;

    public Master()
    {
      leftLegConfig = JsonConvert.DeserializeObject<LeftLegConfig>(File.ReadAllText(@".\Config\LeftLeg.json"));
      rightLegConfig = JsonConvert.DeserializeObject<RightLegConfig>(File.ReadAllText(@".\Config\RightLeg.json"));
    }
  }
}
