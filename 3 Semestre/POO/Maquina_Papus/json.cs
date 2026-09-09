using System.Collections.Generic;

namespace MaquinaPapus
{
    // Estructura que se guarda tal cual en el archivo JSON.
    // Junta las 3 listas de la maquina en un solo objeto para poder
    // leerlas/escribirlas de un solo golpe.
    internal class DatosMaquina
    {
        public List<Productos> Productos { get; set; } = new List<Productos>();
        public List<Papu> Papus { get; set; } = new List<Papu>();
        public List<Money> Money { get; set; } = new List<Money>();
    }
}