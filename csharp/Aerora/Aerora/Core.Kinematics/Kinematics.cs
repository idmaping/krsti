using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Aerora.Core.Kinematics
{
    public class Kinematics : Master
    {
        public string CalculateLeftLeg()
        {
            string result;

            DXL dxl1 = new DXL(1, "XM");
            result = $"{dxl1.GetDegree}";

            return result;
        }
    }
}
