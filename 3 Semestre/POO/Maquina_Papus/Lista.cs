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