using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace weblog
{
    public class Model
    {
        public string? Foo { get; set; }
        public string? Value { get; set; }
        public string? Value1 { get; set; }
        public string? Value2 { get; set; }
        public string? Value5 { get; set; }
        public string? File { get; set; }
        public string? Domain { get; set; }
        public string? User_id { get; set; }
        public string? List_dir { get; set; }
        public string? Command { get; set; }

        public override string ToString() => $"value {Value}, value2 {Value2}";
    }
}
