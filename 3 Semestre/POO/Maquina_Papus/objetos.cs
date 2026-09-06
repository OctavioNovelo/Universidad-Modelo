namespace MaquinaPapus
{
    internal class Money
    {
        // Atributos
        public string Type = "";
        public int Value;
        public int Quantity;


        // Contructor 
        public Money(string Type, int Value, int Quantity)
        {
            this.Type = Type;
            this.Value = Value;
            this.Quantity = Quantity;
        }

        // Metodos
        // El dinero no usa metodos. Es un objeto que no tendria sentido modificar. 
    }


    internal class Papu
    {
        // Atributos
        public string Name { get; set;}
        public int Password;
        
        public List<Money> Dinero { get; private set; }


        // Contructor 
        public Papu(string name, int password, List<Money> dinero = null)
        {
            Name = name;
            Password = password;
            Dinero = new List<Money>
            {
                new Money("Billete", 200, 5), // 1000
                new Money("Billete", 100, 10), // 1000
                new Money("Billete", 50, 10), // 500
                new Money("Billete", 20, 20), // 400
                new Money("Moneda", 20, 10), // 200
                new Money("Moneda", 10, 50), // 500
                new Money("Moneda", 5, 80), // 400
                new Money("Moneda", 2, 20), // 40
                new Money("Moneda", 1, 50) // 50
            };

            if (dinero != null)
            {
                foreach (var item in dinero)
                {
                    var existente = Dinero.Find(m => m.Type == item.Type && m.Value == item.Value);
                    if (existente != null)
                        existente.Quantity = item.Quantity;   
                    else
                        Console.WriteLine("Denominacion invalidad");                    
                }
            }
        }

        // Metodos
        public void ModificarCantidad(int value, int nuevaCantidad)
        {
            Money m = Dinero.Find(x => x.Value == value);
            if (m != null) m.Quantity = nuevaCantidad;

            Console.WriteLine($"Cantidad modificada: {m}");
            Console.WriteLine();
        }

        public int Total()
        {
            int suma = 0;
            foreach (var m in Dinero)
                suma += m.Value * m.Quantity;
            return suma;
        }

        public void Mostrar()
        {
            Console.WriteLine($"--- {Name} ---");
            foreach (var m in Dinero)
                Console.WriteLine($"  {m}");
            Console.WriteLine($"  Total: ${Total():C}");
        }
        
    }

    internal class Productos
    {
        // Atributos
        public string Name = "";
        public int Stock;
        public int Price;
        public string Ubi = "";


        // Contructor 
        public Productos(string name, int price, string ubi)
        {
            this.Name = name;
            Stock = 10;
            this.Price = price;
            this.Ubi = ubi;
        }
        public Productos(string name, int stock, int price, string ubi)
        {
            this.Name = name;
            Stock = stock;
            this.Price = price;
            this.Ubi = ubi;
        }

        // Metodos
        public void Modificar(string name, int price, string ubi, int stock)
        {
            Name = name;
            Price = price;
            Stock = stock;
            Ubi = ubi;
        }    
    }
}