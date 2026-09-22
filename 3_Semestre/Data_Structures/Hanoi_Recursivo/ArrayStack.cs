using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackDev
{
    internal class ArrayStack<T> : IStack<T>
    {
        //datos
        private const int INITIAL_CAPACITY = 4; //tamaño por omision si no se especifica
        private T[] data;
        private int index;

        //propiedades
        public int Capacity  { get; private set; } //son asignables en los constructores

        public int Size => index + 1;

        public bool Empty => index == -1;

        public bool Full => index == data.Length - 1; //se llena pero aun acepta mas numeros

        //constructores
        public ArrayStack()
        {
            Capacity = INITIAL_CAPACITY;
            data = new T[Capacity]; //Crea un arreglo de el tamaño dado
            index = -1;
        }

        public ArrayStack(int capacity)
        {
            Capacity = capacity < INITIAL_CAPACITY ? INITIAL_CAPACITY : capacity;
            data = new T[Capacity]; //Crea un arreglo de el tamaño dado
            index = -1;
        }

        //métodos

        public void Push(T e)
        {
            if (Full)
            {
                T [] newData = new T[Capacity*2];     //creamos un nuevo arreglo con el doble de la capacidad
                Array.Copy(data, newData,Capacity);   //copiamos el data al nuevo data
                Capacity *= 2;                        //modificamos Capacity
                data = newData;                       //convertimos el nuevo data en el data de siempre
            }

            data[++index] = e;
        }

        public T Pop()
        {
            if (Empty)
            {
                throw new InvalidOperationException();
            }

            if(Capacity/2 >= INITIAL_CAPACITY && index == Capacity/5)
            {
                T[] newData = new T[Capacity / 2];     //creamos un nuevo arreglo con el doble de la capacidad
                Array.Copy(data, newData, Size);      //copiamos el data al nuevo data con el tamaño de los datos
                Capacity /= 2;                        //modificamos Capacity
                data = newData;                       //convertimos el nuevo data en el data de siempre
            }

            return data[index--];
        }

        public T Peek()
        {
            if (Empty)
            {
                throw new InvalidOperationException();
            }
            return data[index];
        }

        //ver el elemento que esta en la posicion nivel, sin sacarlo (0 = el del fondo)
        public T PeekAt(int nivel)
        {
            if (nivel < 0 || nivel > index)
            {
                throw new ArgumentOutOfRangeException("nivel");
            }
            return data[nivel];
        }

           #if DEBUG
        public string DataPeek()
        {
            string aux = "[";

            for (int i = 0; i < Size; i++)
            {
                aux += $"{data[i]},";
            }
            aux += "]";
            return aux;
        }
        #endif
    }
}
