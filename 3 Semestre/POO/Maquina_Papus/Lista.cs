using System.Collections;
using System.Collections.Generic;


namespace MaquinaPapus
{
    public class Lista<T> : IEnumerable<T>, IEnumerable
    {
        // Atributos
        private List<T> elementos;

        // Constructores
        public Lista()
        {
            elementos = new List<T>();
        }

        public Lista(int capacidad)
        {
            elementos = new List<T>(capacidad);
        }

        
        // Metodos
        public void Agregar(T elemento)
        {
            elementos.Add(elemento);
        }
        public bool Eliminar(T elemento)
        {
            return elementos.Remove(elemento);
        }
        public void Eliminar(int indice)
        {
            elementos.RemoveAt(indice);
        }
        public T Obtener(int indice)
        {
            return elementos[indice];
        }
        public bool Existe(T elemento)
        {
            return elementos.Contains(elemento);
        }
        public int Size()
        {
            return elementos.Count;
        }
        public bool Empty()
        {
            return elementos.Count == 0;
        }

        public void Clear()
        {
            elementos.Clear();
        }

        // Convierte la Lista a un List<T> normal (util para serializar a JSON).
        public List<T> ToList()
        {
            return new List<T>(elementos);
        }

        // Reemplaza todo el contenido con los valores dados (util al cargar desde JSON).
        public void CargarDesde(IEnumerable<T> valores)
        {
            elementos.Clear();
            if (valores != null)
                elementos.AddRange(valores);
        }

        
        public T this[int indice]
        {
            get { return elementos[indice]; }
            set { elementos[indice] = value; }
        }

        // Permite utilizar foreach
        public IEnumerator<T> GetEnumerator()
        {
            return elementos.GetEnumerator();
        }

        // Implementación requerida por IEnumerable
        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }
}