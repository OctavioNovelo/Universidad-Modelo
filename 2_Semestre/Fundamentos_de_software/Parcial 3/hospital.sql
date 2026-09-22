-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:33065
-- Tiempo de generación: 19-11-2025 a las 00:33:08
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hospital`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `ID_Cita` int(5) NOT NULL,
  `Fecha` date NOT NULL,
  `Hora` time NOT NULL,
  `ID_Paciente` int(5) NOT NULL,
  `Cédula_Profesional` int(8) NOT NULL,
  `Estado` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `diagnóstico`
--

CREATE TABLE `diagnóstico` (
  `ID_Diagnóstico` int(8) NOT NULL,
  `Nombre` varchar(20) NOT NULL,
  `Descripción` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dirección`
--

CREATE TABLE `dirección` (
  `Calle` int(3) NOT NULL,
  `Número` int(3) NOT NULL,
  `Colonia` varchar(20) NOT NULL,
  `Estado` varchar(8) NOT NULL,
  `Código_Postal` int(5) NOT NULL,
  `Nombre_Propietario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial médico`
--

CREATE TABLE `historial médico` (
  `ID_Registro` int(8) NOT NULL,
  `ID_Paciente` int(8) NOT NULL,
  `Fecha` date NOT NULL,
  `Cédula_Profesional` int(8) NOT NULL,
  `ID_Diagnóstico` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicamentos`
--

CREATE TABLE `medicamentos` (
  `ID_Medicamento` int(8) NOT NULL,
  `Nombre_Comercial` varchar(20) NOT NULL,
  `Principio_Activo` varchar(20) NOT NULL,
  `Dosis` int(3) NOT NULL,
  `Stock` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `médicos`
--

CREATE TABLE `médicos` (
  `Cédula_Profesional` int(8) NOT NULL,
  `Nombres` varchar(20) NOT NULL,
  `Especialidad` varchar(20) NOT NULL,
  `Área_Trabajo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paciente`
--

CREATE TABLE `paciente` (
  `ID` int(5) NOT NULL,
  `Nombre` varchar(20) NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `Dirección` varchar(200) NOT NULL,
  `Teléfono` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`ID_Cita`),
  ADD KEY `Cédula_Profesional` (`Cédula_Profesional`),
  ADD KEY `ID_Paciente` (`ID_Paciente`);

--
-- Indices de la tabla `diagnóstico`
--
ALTER TABLE `diagnóstico`
  ADD PRIMARY KEY (`ID_Diagnóstico`);

--
-- Indices de la tabla `dirección`
--
ALTER TABLE `dirección`
  ADD PRIMARY KEY (`Nombre_Propietario`);

--
-- Indices de la tabla `historial médico`
--
ALTER TABLE `historial médico`
  ADD KEY `ID_Paciente` (`ID_Paciente`,`Cédula_Profesional`,`ID_Diagnóstico`),
  ADD KEY `Cédula_Profesional` (`Cédula_Profesional`),
  ADD KEY `ID_Diagnóstico` (`ID_Diagnóstico`);

--
-- Indices de la tabla `médicos`
--
ALTER TABLE `médicos`
  ADD PRIMARY KEY (`Cédula_Profesional`);

--
-- Indices de la tabla `paciente`
--
ALTER TABLE `paciente`
  ADD PRIMARY KEY (`ID`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`Cédula_Profesional`) REFERENCES `médicos` (`Cédula_Profesional`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `historial médico`
--
ALTER TABLE `historial médico`
  ADD CONSTRAINT `historial médico_ibfk_1` FOREIGN KEY (`Cédula_Profesional`) REFERENCES `médicos` (`Cédula_Profesional`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `historial médico_ibfk_2` FOREIGN KEY (`ID_Paciente`) REFERENCES `paciente` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `historial médico_ibfk_3` FOREIGN KEY (`ID_Diagnóstico`) REFERENCES `diagnóstico` (`ID_Diagnóstico`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `paciente`
--
ALTER TABLE `paciente`
  ADD CONSTRAINT `paciente_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `citas` (`ID_Paciente`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
