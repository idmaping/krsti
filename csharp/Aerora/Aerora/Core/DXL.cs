using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Aerora.Core
{
  class DXL
  {
    private double _value;
    private int _id;
    private string _type;
    public double SetDegree
    {
      set
      {
        if (value > 0)
        {
          double temp = value;
          while (temp >= 360)
          {
            temp -= 360;
          }
          _value = temp;
        }
        else if (value < 0)
        {
          double temp = value;
          while (_value < 0)
          {
            temp = 360 + temp;
          }
          _value = temp;
        }
      }
    }
    public double GetDegree
    {
      get { return _value; }
    }



    public int ID
    {
      get
      {
        return _id;
      }
      set
      {
        _id = value;
      }
    }
    public string Type
    {
      get
      {
        return _type;
      }
      set
      {
        _type = value;
      }
    }
    
    public DXL(int id, string type)
    {
      ID = id;
      Type = type;
    }

  }
}
