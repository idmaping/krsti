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
    public int JointA_DXLID { get; set; }
    public string JointA_DXLType { get; set; }
    public int JointB_DXLID { get; set; }
    public string JointB_DXLType { get; set; }
    public int JointC_DXLID { get; set; }
    public string JointC_DXLType { get; set; }
    public int JointD_DXLID { get; set; }
    public string JointD_DXLType { get; set; }
    public int JointE_DXLID { get; set; }
    public string JointE_DXLType { get; set; }
    public int JointF_DXLID { get; set; }
    public string JointF_DXLType { get; set; }
  }

}
