using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;

namespace MaquinaPapus
{
    internal class CLI
    {
        public static Lista<Productos> productos = new Lista<Productos>();
        public static Lista<Papu> papus = new Lista<Papu>();
        public static Lista<Money> money = new Lista<Money>();

        // Ruta del archivo donde se guardan los datos de la maquina.
        private static readonly string RutaArchivo =
            Path.Combine(AppContext.BaseDirectory, "maquina_papus.json");

        private static readonly JsonSerializerOptions JsonOpciones = new JsonSerializerOptions
        {
            WriteIndented = true,           // Para que el .json sea legible
            IncludeFields = true,           // Money y Productos guardan datos en campos publicos, no propiedades
            PropertyNameCaseInsensitive = true
        };

        // Se ejecuta una sola vez, al usarse la clase CLI por primera vez.
        static CLI()
        {
            // Si ya existe un archivo de datos guardado, lo cargamos.
            // Si no existe (o esta corrupto), se usan los valores default.
            if (!CargarDatos())
            {
                InicializarProductos();
                InicializarPapus();
                InicializarDineroMaquina();
                GuardarDatos();
            }
        }

        // ---------------------------------------------------------
        //  Persistencia en JSON
        // ---------------------------------------------------------

        // Intenta cargar productos, papus y dinero desde el archivo JSON.
        // Devuelve true si se cargo correctamente.
        public static bool CargarDatos()
        {
            try
            {
                if (!File.Exists(RutaArchivo))
                    return false;

                string json = File.ReadAllText(RutaArchivo);
                DatosMaquina datos = JsonSerializer.Deserialize<DatosMaquina>(json, JsonOpciones);

                if (datos == null)
                    return false;

                productos.CargarDesde(datos.Productos);
                papus.CargarDesde(datos.Papus);
                money.CargarDesde(datos.Money);

                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"No se pudo leer {Path.GetFileName(RutaArchivo)}, se usaran los valores default. ({ex.Message})");
                return false;
            }
        }

        // Guarda productos, papus y dinero en el archivo JSON.
        // Se llama automaticamente despues de cada operacion que modifica datos.
        public static void GuardarDatos()
        {
            try
            {
                var datos = new DatosMaquina
                {
                    Productos = productos.ToList(),
                    Papus = papus.ToList(),
                    Money = money.ToList()
                };

                string json = JsonSerializer.Serialize(datos, JsonOpciones);
                File.WriteAllText(RutaArchivo, json);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"No se pudo guardar {Path.GetFileName(RutaArchivo)}: {ex.Message}");
            }
        }

        // ---------------------------------------------------------
        //  Inicializacion de datos por default
        // ---------------------------------------------------------

        private static void InicializarProductos()
        {
            // Constructor usado: Productos(name, stock, price, ubi)
            // Columnas validas: A-E    Filas validas: 1-6
            productos.Agregar(new Productos("Coca Cola", 10, 18, "A1"));
            productos.Agregar(new Productos("Sprite", 10, 18, "A2"));
            productos.Agregar(new Productos("Agua Ciel", 15, 15, "A3"));
            productos.Agregar(new Productos("Jugo Del Valle", 8, 20, "A4"));
            productos.Agregar(new Productos("Gatorade", 6, 25, "A5"));

            productos.Agregar(new Productos("Sabritas Original", 10, 17, "B1"));
            productos.Agregar(new Productos("Doritos Nacho", 10, 18, "B2"));
            productos.Agregar(new Productos("Cheetos Torciditos", 10, 17, "B3"));
            productos.Agregar(new Productos("Ruffles Queso", 8, 18, "B4"));
            productos.Agregar(new Productos("Cheetos Flamin Hot", 10, 19, "B5"));

            productos.Agregar(new Productos("Gansito", 10, 16, "C1"));
            productos.Agregar(new Productos("Choco Roles", 10, 15, "C2"));
            productos.Agregar(new Productos("Barritas Marinela", 10, 14, "C3"));
            productos.Agregar(new Productos("Oreo", 10, 15, "C4"));
            productos.Agregar(new Productos("Principe", 10, 15, "C5"));

            productos.Agregar(new Productos("Snickers", 10, 20, "D1"));
            productos.Agregar(new Productos("Kit Kat", 10, 20, "D2"));
            productos.Agregar(new Productos("Skittles", 10, 17, "D3"));
            productos.Agregar(new Productos("M&Ms", 10, 18, "D4"));
            productos.Agregar(new Productos("Trident", 15, 12, "D5"));

            // La fila E queda vacia a proposito (se vera como [VACIO] en la matriz).
        }

        private static void InicializarPapus()
        {
            // Cada papu (distribuidor) inicia con un fondo propio distinto.
            // Las denominaciones que no se especifican aqui usan el default
            // definido dentro del constructor de Papu.
            var dineroJuan = new List<Money>
            {
                new Money("Billete", 200, 3),
                new Money("Billete", 100, 5),
                new Money("Moneda", 10, 20)
            };

            var dineroPedro = new List<Money>
            {
                new Money("Billete", 100, 8),
                new Money("Moneda", 5, 40),
                new Money("Moneda", 1, 60)
            };

            var dineroLuis = new List<Money>
            {
                new Money("Billete", 50, 15),
                new Money("Moneda", 20, 15),
                new Money("Moneda", 2, 25)
            };

            papus.Agregar(new Papu("Juan", 1111, dineroJuan));
            papus.Agregar(new Papu("Pedro", 2222, dineroPedro));
            papus.Agregar(new Papu("Luis", 3333, dineroLuis));
        }

        private static void InicializarDineroMaquina()
        {
            // Fondo inicial de cambio con el que arranca la maquina expendedora.
            money.Agregar(new Money("Billete", 200, 0));
            money.Agregar(new Money("Billete", 100, 0));
            money.Agregar(new Money("Billete", 50, 2));
            money.Agregar(new Money("Billete", 20, 5));
            money.Agregar(new Money("Moneda", 20, 5));
            money.Agregar(new Money("Moneda", 10, 10));
            money.Agregar(new Money("Moneda", 5, 20));
            money.Agregar(new Money("Moneda", 2, 20));
            money.Agregar(new Money("Moneda", 1, 30));
        }

        // ---------------------------------------------------------
        //  Utilidades
        // ---------------------------------------------------------

        public static string Normalizer(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
                return "";

            return input
                .Trim()
                .ToLower()
                .Replace(" ", "")
                .Replace("ñ", "n")
                .Replace("á", "a")
                .Replace("é", "e")
                .Replace("í", "i")
                .Replace("ó", "o")
                .Replace("ú", "u")
                .Replace("ü", "u");
        }

        // ---------------------------------------------------------
        //  CLI principal (cliente)
        // ---------------------------------------------------------

        public static void Commmand_Line_Interface()
        {
            Console.Write("> ");
            string input = Normalizer(Console.ReadLine());
            switch (input)
            {
                case "clear": Console.Clear(); break;
                case "exit": GuardarDatos(); Environment.Exit(0); break;
                case "help": Mostrar("help"); break;
                case "productos": Mostrar("productos"); break;
                case "buy": Buy(); break;
                case "papu":
                {
                    Console.WriteLine("password:");
                    if (int.TryParse(Console.ReadLine(), out int password))
                    {
                        Papu papu = Admin_Verif(password, papus);
                        Admin_Command_Line_Interface(papu);
                    }
                    else
                    {
                        Console.WriteLine("Password invalida.");
                    }
                    break;
                }
                default: Console.WriteLine($"Papu: Unknow Command: {input}"); break;
            }
        }

        // Devuelve el papu cuya password coincide, o null si ninguna coincide.
        public static Papu Admin_Verif(int password, Lista<Papu> distribuidores)
        {
            for (int i = 0; i < distribuidores.Size(); i++)
            {
                if (distribuidores[i].Password == password)
                {
                    return distribuidores[i];
                }
            }

            return null;
        }

        // ---------------------------------------------------------
        //  CLI de administracion (papu)
        // ---------------------------------------------------------

        public static void Admin_Command_Line_Interface(Papu papu)
        {
            if (papu == null)
            {
                Console.WriteLine("Incorrect Password");
                return;
            }

            Console.WriteLine($"Correct Password. Bienvenido {papu.Name}");
            bool salir = false;

            while (!salir)
            {
                Console.Write("papu> ");
                string input = Normalizer(Console.ReadLine());
                switch (input)
                {
                    case "clear": Console.Clear(); break;
                    case "exit": GuardarDatos(); salir = true; break; // Salir de papu_CLI
                    case "help": Mostrar("papu_help"); break;
                    case "productos": Mostrar("productos"); break;
                    case "buy": Buy(); break;
                    case "modprod": Mod_Prod(); break; // Modificar un producto
                    case "modmoney": Mod_Money(papu); break; // Rellenar cambio / retirar ganancias
                    case "modpapus": Mod_Papu(papu); break; // Modificar datos del propio papu
                    default: Console.WriteLine($"Papu: Comando desconocido: {input}"); break;
                }
            }
        }

        // Todos los comandos mostrar son arreglos.
        public static void Mostrar(string input)
        {
            switch (input)
            {
                case "productos":
                    Productos[,] matriz = new Productos[6, 5];
                    foreach (Productos producto in productos)
                    {
                        char columna = char.ToUpper(producto.Ubi[0]);
                        int fila = int.Parse(producto.Ubi[1].ToString());

                        int x = columna - 'A';
                        int y = fila - 1;

                        if (y >= 0 && y < 6 && x >= 0 && x < 5)
                            matriz[y, x] = producto;
                    }

                    // Imprimir la matriz
                    for (int fila = 0; fila < 6; fila++)
                    {
                        for (int columna = 0; columna < 5; columna++)
                        {
                            Productos p = matriz[fila, columna];
                            if (p != null)
                            {
                                Console.Write($"[{p.Ubi} {p.Name} ${p.Price} ({p.Stock})]\t");
                            }
                            else
                            {
                                Console.Write("[VACIO]\t");
                            }
                        }

                        Console.WriteLine();
                    }

                    break;

                case "papus":
                    for (int i = 0; i < papus.Size(); i++)
                    {
                        papus[i].Mostrar();
                    }
                    break;

                case "money":
                    Console.WriteLine("--- Dinero de la maquina ---");
                    int total = 0;
                    for (int i = 0; i < money.Size(); i++)
                    {
                        Money m = money[i];
                        Console.WriteLine($"  {m}");
                        total += m.Value * m.Quantity;
                    }
                    Console.WriteLine($"  Total: ${total}");
                    Console.WriteLine();
                    break;

                case "help":
                    Console.WriteLine("///////// Commands /////////");
                    Console.WriteLine();
                    Console.WriteLine("-- help       Show all commands");
                    Console.WriteLine();
                    Console.WriteLine("-- clear      Clean the shell");
                    Console.WriteLine();
                    Console.WriteLine("-- productos  Show all products");
                    Console.WriteLine();
                    Console.WriteLine("-- buy        Buy a product");
                    Console.WriteLine();
                    Console.WriteLine("-- papu       Enter papu mode");
                    Console.WriteLine();
                    Console.WriteLine("-- exit       Exit the program");
                    Console.WriteLine();
                    Console.WriteLine("///////////////////////////");
                    break;

                case "papu_help":
                    Console.WriteLine("///////// Papu Commands /////////");
                    Console.WriteLine();
                    Console.WriteLine("-- help       Show all commands");
                    Console.WriteLine();
                    Console.WriteLine("-- clear      Clean the shell");
                    Console.WriteLine();
                    Console.WriteLine("-- exit       Exit the Papu shell");
                    Console.WriteLine();
                    Console.WriteLine("-- modprod    Modify the products");
                    Console.WriteLine();
                    Console.WriteLine("-- modmoney   Modify the money");
                    Console.WriteLine();
                    Console.WriteLine("-- modpapus   Modify the papus");
                    Console.WriteLine();
                    Console.WriteLine("-- productos  Show all products");
                    Console.WriteLine();
                    Console.WriteLine("-- buy        Buy a product");
                    Console.WriteLine();
                    Console.WriteLine("///////////////////////////");
                    break;

                default:
                    Console.WriteLine("Comando no reconocido.");
                    break;
            }
        }

        // ---------------------------------------------------------
        //  Compra
        // ---------------------------------------------------------

        public static void Buy()
        {
            Mostrar("productos");
            Console.WriteLine("Ingresa la ubicacion del producto:");
            string ubi = (Console.ReadLine() ?? "").Trim().ToUpper();

            Productos producto = null;
            foreach (var p in productos)
            {
                if (p.Ubi.ToUpper() == ubi)
                {
                    producto = p;
                    break;
                }
            }

            if (producto == null)
            {
                Console.WriteLine("Producto no encontrado.");
                return;
            }

            if (producto.Stock <= 0)
            {
                Console.WriteLine("Producto agotado.");
                return;
            }

            Console.WriteLine($"{producto.Name} - ${producto.Price}");
            Console.WriteLine("Ingresa el monto pagado:");
            if (!int.TryParse(Console.ReadLine(), out int pagado))
            {
                Console.WriteLine("Monto invalido.");
                return;
            }

            if (pagado < producto.Price)
            {
                Console.WriteLine("Pago insuficiente.");
                return;
            }

            int cambio = pagado - producto.Price;

            if (cambio > 0 && !HayCambioSuficiente(cambio))
            {
                Console.WriteLine("La maquina no tiene cambio suficiente. Compra cancelada.");
                return;
            }

            // Quitar -1 al stock y sumar el pago a las ganancias de la maquina.
            if (cambio > 0)
            {
                EntregarCambio(cambio);
            }

            AgregarDineroMaquina(pagado);
            producto.Stock--;
            GuardarDatos();

            Console.WriteLine($"Aqui tienes tu {producto.Name}. Cambio: ${cambio}");
            Console.WriteLine();
        }

        // ---------------------------------------------------------
        //  Modificaciones (admin)
        // ---------------------------------------------------------

        public static void Mod_Prod()
        {
            // Modificar un producto es: Mod Name, Mod Stock, Mod Price, Mod Ubi
            Mostrar("productos");
            Console.WriteLine("Modificar: (ubi o nombre)");
            string input = Console.ReadLine() ?? "";
            string normalizado = Normalizer(input);
            string ubiInput = input.Trim().ToUpper();

            Productos encontrado = null;
            foreach (var p in productos)
            {
                if (Normalizer(p.Name) == normalizado || p.Ubi.ToUpper() == ubiInput)
                {
                    encontrado = p;
                    break;
                }
            }

            if (encontrado == null)
            {
                Console.WriteLine("Producto no encontrado.");
                return;
            }

            Console.WriteLine($"Editando: {encontrado.Name} ({encontrado.Ubi})");

            Console.WriteLine($"Nuevo nombre (actual: {encontrado.Name}, enter para no cambiar):");
            string nombre = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(nombre)) nombre = encontrado.Name;

            Console.WriteLine($"Nuevo precio (actual: {encontrado.Price}, enter para no cambiar):");
            string precioStr = Console.ReadLine();
            int precio = (!string.IsNullOrWhiteSpace(precioStr) && int.TryParse(precioStr, out int nuevoPrecio))
                ? nuevoPrecio
                : encontrado.Price;

            Console.WriteLine($"Nueva ubicacion (actual: {encontrado.Ubi}, enter para no cambiar):");
            string ubi = Console.ReadLine();
            ubi = string.IsNullOrWhiteSpace(ubi) ? encontrado.Ubi : ubi.Trim().ToUpper();

            Console.WriteLine($"Nuevo stock (actual: {encontrado.Stock}, enter para no cambiar):");
            string stockStr = Console.ReadLine();
            int stock = (!string.IsNullOrWhiteSpace(stockStr) && int.TryParse(stockStr, out int nuevoStock))
                ? nuevoStock
                : encontrado.Stock;

            encontrado.Modificar(nombre, precio, ubi, stock);
            GuardarDatos();
            Console.WriteLine("Producto modificado correctamente.");
            Console.WriteLine();
        }

        public static void Mod_Money(Papu papu)
        {
            // Quitar dinero de lo que tiene el papu y rellenar la maquina expendedora,
            // o agregar dinero sobrante (ganancias) de la maquina expendedora al papu.
            Console.WriteLine("1. Ver dinero de la maquina");
            Console.WriteLine("2. Rellenar cambio de la maquina");
            Console.WriteLine("3. Retirar ganancias de la maquina");
            string opcion = Console.ReadLine();

            switch (opcion)
            {
                case "1":
                    Mostrar("money");
                    break;

                case "2":
                    TransferirDinero(papu.Dinero, ListaAList(money), "Cambio depositado en la maquina.");
                    break;

                case "3":
                    TransferirDinero(ListaAList(money), papu.Dinero, "Ganancia retirada.");
                    break;

                default:
                    Console.WriteLine("Opcion invalida.");
                    break;
            }
        }

        public static void Mod_Papu(Papu papu)
        {
            // Modificar un papu es: Mod su nombre, Mod su password, Ver su dinero.
            Console.WriteLine($"--- {papu.Name} ---");
            Console.WriteLine("1. Cambiar nombre");
            Console.WriteLine("2. Cambiar password");
            Console.WriteLine("3. Ver mi dinero");
            string opcion = Console.ReadLine();

            switch (opcion)
            {
                case "1":
                    Console.WriteLine("Nuevo nombre:");
                    string nuevoNombre = Console.ReadLine();
                    if (!string.IsNullOrWhiteSpace(nuevoNombre))
                    {
                        papu.Name = nuevoNombre;
                        GuardarDatos();
                        Console.WriteLine("Nombre actualizado.");
                    }
                    break;

                case "2":
                    Console.WriteLine("Nueva password:");
                    if (int.TryParse(Console.ReadLine(), out int nuevaPass))
                    {
                        papu.Password = nuevaPass;
                        GuardarDatos();
                        Console.WriteLine("Password actualizada.");
                    }
                    else
                    {
                        Console.WriteLine("Password invalida.");
                    }
                    break;

                case "3":
                    papu.Mostrar();
                    break;

                default:
                    Console.WriteLine("Opcion invalida.");
                    break;
            }

            Console.WriteLine();
        }

        // ---------------------------------------------------------
        //  Helpers de dinero
        // ---------------------------------------------------------

        private static List<Money> ListaAList(Lista<Money> lista)
        {
            var resultado = new List<Money>();
            foreach (var m in lista) resultado.Add(m);
            return resultado;
        }

        // Mueve "cantidad" piezas de una denominacion de una lista de dinero a otra.
        private static void TransferirDinero(List<Money> origen, List<Money> destino, string mensajeExito)
        {
            Console.WriteLine("Que denominacion? (valor):");
            if (!int.TryParse(Console.ReadLine(), out int valor))
            {
                Console.WriteLine("Valor invalido.");
                return;
            }

            Console.WriteLine("Cuantas piezas?");
            if (!int.TryParse(Console.ReadLine(), out int cantidad) || cantidad <= 0)
            {
                Console.WriteLine("Cantidad invalida.");
                return;
            }

            Money monedaOrigen = origen.Find(m => m.Value == valor);
            Money monedaDestino = destino.Find(m => m.Value == valor);

            if (monedaOrigen == null || monedaDestino == null)
            {
                Console.WriteLine("Denominacion invalida.");
                return;
            }

            if (monedaOrigen.Quantity < cantidad)
            {
                Console.WriteLine("No hay suficiente de esa denominacion.");
                return;
            }

            monedaOrigen.Quantity -= cantidad;
            monedaDestino.Quantity += cantidad;
            GuardarDatos();
            Console.WriteLine(mensajeExito);
        }

        // Revisa (con un algoritmo greedy) si la maquina puede dar el cambio exacto.
        private static bool HayCambioSuficiente(int monto)
        {
            int restante = monto;
            var ordenado = money.OrderByDescending(m => m.Value).ToList();

            foreach (var m in ordenado)
            {
                if (restante <= 0) break;
                int usar = Math.Min(restante / m.Value, m.Quantity);
                restante -= usar * m.Value;
            }

            return restante == 0;
        }

        // Descuenta de la maquina las piezas usadas para dar el cambio.
        private static void EntregarCambio(int monto)
        {
            int restante = monto;
            var ordenado = money.OrderByDescending(m => m.Value).ToList();

            foreach (var m in ordenado)
            {
                if (restante <= 0) break;
                int usar = Math.Min(restante / m.Value, m.Quantity);
                if (usar > 0)
                {
                    m.Quantity -= usar;
                    restante -= usar * m.Value;
                }
            }
        }

        // Suma el pago del cliente al dinero de la maquina (ganancias).
        private static void AgregarDineroMaquina(int monto)
        {
            int restante = monto;
            var ordenado = money.OrderByDescending(m => m.Value).ToList();

            foreach (var m in ordenado)
            {
                if (restante <= 0) break;
                int usar = restante / m.Value;
                if (usar > 0)
                {
                    m.Quantity += usar;
                    restante -= usar * m.Value;
                }
            }
        }
    }
}