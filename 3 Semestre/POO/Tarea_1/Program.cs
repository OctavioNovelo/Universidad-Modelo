// See https://aka.ms/new-console-template for more information

// Avr puta falta arreglar lo sig:
// - No se porque no puedes crear mas de 2 papus
// - Atacar hay que escoger que papu ataca a cada papu
// - Tratar de limpiar la pantalla cada que se escoge una opcion
Papu miPapu = null;
Papu enemigo = null;

bool jugando = true;

while (jugando)
{
    Console.WriteLine();
    Console.WriteLine("--- Menú ---");
    Console.WriteLine("1. Crear Papu");
    Console.WriteLine("2. Stats");
    Console.WriteLine("3. Atacar");
    Console.WriteLine("4. Salir");
    Console.Write("Elige una opción: ");

    string opcion = Console.ReadLine();

    switch (opcion)
    {
        case "1":
            if (miPapu == null)
                miPapu = Tarea_1_Metod.Crear();
            else if (enemigo == null)
                enemigo = Tarea_1_Metod.Crear();
            else
                Console.WriteLine("Ya tienes dos Papus creados.");
            break;

        case "2":
            if (miPapu != null) Tarea_1_Metod.Print(miPapu);
            if (enemigo != null) Tarea_1_Metod.Print(enemigo);
            if (miPapu == null && enemigo == null)
                Console.WriteLine("No hay Papus.");
            break;

        case "3":
            if (miPapu != null && enemigo != null)
                miPapu.Atacar(enemigo);
            else
                Console.WriteLine("No hay papus.");
            break;

        case "4":
            jugando = false;
            Console.WriteLine("Chao!");
            break;

        default:
            Console.WriteLine("Opción inválida, intenta de nuevo.");
            break;
    }
}