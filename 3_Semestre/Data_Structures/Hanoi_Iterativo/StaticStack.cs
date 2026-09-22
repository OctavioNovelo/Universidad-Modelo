using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackDev
{
    internal class StaticStack<T> : IStack<T>
    {
        //datos
        private T[] data;
        private int index;

        //propiedad
        public int Size => index + 1; //de solo lectura

        public bool Empty => index == -1;

        public bool Full => index == data.Length -1;  //En c# los arreglos saben su tamaño con .Length

        //constructor
        public StaticStack(int capacity)
        {
            data = new T[capacity]; //Crea un arreglo de el tamaño dado
            index = -1;
        }

        public StaticStack(int capacity, int h)
        {
            data = new T[capacity];

            for (int i = capacity - 1; i >= 0; i--)
            {
                T papu = (T)(object)h;
                data[i] = papu;
                h++;
            }

            index = capacity - 1;
        }


        //metodos
        public T Peek()
        {
            if (Empty)
            {
                throw new InvalidOperationException();
            }
            return data[index];
        }

        public T Pop()
        {
            if (Empty)
            {
                throw new InvalidOperationException();
            }
            return data[index--];
        }

        public void Push(T e)
        {
            if(Full)
            {
                throw new IndexOutOfRangeException("index");
            }

            data[++index] = e;  //aqui se le suma a un index y se agrega el elemento

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

            for(int i = 0; i < Size; i++)
            {
                aux += $"{data[i]},";
            }
            aux += "]";
            return aux;
        }
        #endif
    }
}
