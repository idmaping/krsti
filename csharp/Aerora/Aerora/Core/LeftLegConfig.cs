using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Aerora.Core
{
  public class LeftLegConfig : ILegConfig
  {
    public double Femur { get; set; }
    public double Tibia { get; set; }
    public bool SimMode { get; set; }
    public int IDJointA { get; set; }
    public int IDJointB { get; set; }
    public int IDJointC { get; set; }
    public int IDJointD { get; set; }
    public int IDJointE { get; set; }
    public int IDJointF { get; set; }
  }

}
