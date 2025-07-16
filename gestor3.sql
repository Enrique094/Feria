-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-07-2025 a las 18:03:43
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
-- Base de datos: `gestor3`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `abono_venta`
--

CREATE TABLE `abono_venta` (
  `id_abono` int(11) NOT NULL,
  `id_factura_venta` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_cobrador` int(11) NOT NULL,
  `monto_abonado` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(20) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id_categoria`, `nombre`, `descripcion`) VALUES
(1, 'Ropa', 'Vestidos, uniformes'),
(2, 'Electrodomesticos', 'Dispositivos electrónicos'),
(3, 'Accesorios', 'Accesorios para hombre o mujer');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(20) DEFAULT NULL,
  `apellido` varchar(20) DEFAULT NULL,
  `id_rango` int(11) DEFAULT NULL,
  `tel` varchar(15) DEFAULT NULL,
  `dui` varchar(10) DEFAULT NULL,
  `correo` varchar(30) DEFAULT NULL,
  `direccion` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `apellido`, `id_rango`, `tel`, `dui`, `correo`, `direccion`) VALUES
(1, 'Jairick', 'Salvastian', 2, '74747474', '232323-2', 'Jairosebastian@gmail.com', 'Valle verde 2, Apopa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cobrador`
--

CREATE TABLE `cobrador` (
  `id_cobrador` int(11) NOT NULL,
  `nombre` varchar(20) DEFAULT NULL,
  `apellido` varchar(20) DEFAULT NULL,
  `tel` varchar(15) DEFAULT NULL,
  `id_rango` int(11) DEFAULT NULL,
  `id_zona` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cobrador`
--

INSERT INTO `cobrador` (`id_cobrador`, `nombre`, `apellido`, `tel`, `id_rango`, `id_zona`) VALUES
(1, 'Omar Enrique', 'Ventura', '76379499', 4, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cobrador_cliente`
--

CREATE TABLE `cobrador_cliente` (
  `id_cobrador` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contrato`
--

CREATE TABLE `contrato` (
  `id_contrato` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_vende` int(11) NOT NULL,
  `id_cobrador` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_cobro`
--

CREATE TABLE `factura_cobro` (
  `id_factura_cobro` int(11) NOT NULL,
  `id_cobrador` int(11) NOT NULL,
  `id_zona` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_venta`
--

CREATE TABLE `factura_venta` (
  `id_factura_venta` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_vende` int(11) NOT NULL,
  `id_product` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `Precio_Mensual` decimal(10,0) NOT NULL,
  `Cuotas` bit(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_product` int(11) NOT NULL,
  `id_catego` int(11) NOT NULL,
  `nombre` varchar(30) DEFAULT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `imagen` tinyint(1) DEFAULT 0,
  `imagen_blob` longblob DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `Intereses` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_product`, `id_catego`, `nombre`, `descripcion`, `precio`, `imagen`, `imagen_blob`, `stock`, `Intereses`) VALUES
(2, 1, 'Camisa', 'Camisa con estampado para Hombre', 24.99, 1, 0xffd8ffe000104a46494600010100000100010000ffdb00840009060710111215130f0e0f100d1010150f0f0f0f1010100f100f1512171715151515181d2820181a261d15152131212629372e3232171f333835354328392f2b010a0a0a0e0d0e170f10172d1d151d2d2d2e2e2d2e2b2d2b372d2d372d37373737342b2b372d2e37372d2f2b2d3737303732372b2b2b2c2d2b37322d3737372d31ffc000110800d900e803012200021101031101ffc4001c0001000202030100000000000000000000000407020301060805ffc4004910000103020304060604090b0500000000010002030411052131060712411422325161710813728191b1234252d1243443628292a1b3c115172533556374a3b2d2d3447393c2f0ffc4001a010101010003010000000000000000000000010203050704ffc4002511010100020103040105000000000000000001021103041231142141615105131581b1ffda000c03010002110311003f00bc511101111011110111101111011145c4311829dbc7513c5047f6e691b1b7e2e282522e975fbd4c1627861ae6c879ba08e5998d1e2e63483eebafaf86ed961951fd4e214af27ea9998c7fea38823e083eea2c6391ae176b83877820851eb71182104cf3c31346a65918c03e2504a45d2f10dea60d0b834d70909362608e5998d1de5cc691f0375d8307da3a2abfc56b29e736b96c7235cf03c59a8f7841f511110111101111011110111101111011110111101111011155bb5fbe4a7a67be1a287a54cc25a6673b86943c646c46725bc2c3c505a4baa6d36f0f0ca0bb65a91254375a7a7fa5981ee701930fb442a1b1edbfc52b2e25ac7b223f91a6fa08edddd5eb387b4e2bab0681a0b2ba4daceda3df4574d76d144ca38b301eeb4d50477e7d46f958f9aadf11ad9aa1e64a99a49e53f9499ee7bad7d013a0f0192d375c2a8d03b5fa2b6165fb8f98584a3470e5af92d80a0e1adb7672f2cbe4b1f563b87c16d5c1418596701b105a4b5edb16b9a4b5cd23982330562e2b96a0eeb816f4b17a4b03502aa21f52ada6436f09059f7f32558d80efbe8a4b36b29e6a47f37b7f0886fe6d01e3f57dea8725604268dbd7f83e3d4956de2a4aa8671cfd548d739bed37569f0217d15e3089ce6383d8e732469bb5ec716bda7bc38661583b25bdeafa5735b56e35b4b701dc7c22a58def6499711f076bde14d2ede8e45130ac462a98639e0787c13303e378b8bb4f783983c883a594b5144444044440444404444044440445f2b6a31d8a82965a99bb3137aade724872630789240fda82b8df6edbbe11d0295fc324ad06ae46921cc89dd989a4685c2e4f85bed65468eeeec87c4a998a57495133e699dc534af74d21e5c4e3a0ee02f60390002872647e1fc5699640a15cae0a0c51172107042c032da69ddf72dab8b20c2eb82f593dab0b20e005b170b241c22e57050160751e6b35aa4398f6bee416dee2b6c3d4ccec3e77fd0cee2fa52e3932723ad1f8070171f9c0f372be578bc3cb5e1cd716b8105ae69b39ae69b820f220e6bd3fbb1db1189d282f2d15b05a3a960cae6dd5940fb2e009f021c3929563b8a2228a222202222022220222202f3a6f776c7a7d57a885d7a1a4710d2349a7170f93c40cdadfd23cd77ddf3edb7458ba1d3bad5750cfa57b4e70539c8f93dd981dc2e7baf4242323f01e4ac4ad529ed7b3fc56329b8bf805c4e723e2570dec0551b5a742b9705ae1397915b8e8835ae42c5737b0fda8325cab4307dcad4cd132476214ac12303da228df50db1171d7e2683ee5d4f6cb63e5c3aa194e6a21a87c8ce31eaaed7b05ff0028c24f05f506f9d8f726e2e38dcac926ed75972c17d77e0525ae1ec2efb39dbe2b5d2e0b23c5c90cee04127dfdcb87d4716b7dcec7f87ebbba61fb5777dfe3fdf0f9a172a455d1be23675b3d1c342a3b972e394ca6e787c1cbc59f16770ce6b29e6570b92810aac0028f21cdbe67e6a428d26a106d9f91eeb2ec1b15b4d261d54ca88eee60ea4f1036f5b01ed37cc6447880be13c5dbee5ae177dc83d9586d7c551132681e1f0cac1246f1a169171e47c149540ee5b6dba2ca28aa5f6a4a87fd03dc7286a1df57c1af3f077b455fcb2d0888808888088880be36d6ed14387533ea26cc3470c718ed4b29ecb1be7dfc802792fb2a91dfae1189c9289f80cb8642c0231092e30b88fa47cacd6e4fd6170001a730aab16c465aa9a49a77714f33cbe4772b9e40726816007700b0b5805aa1175b1e755a650e6ecfbd731f6079958bfb3ef59b075020e213aa93c9456e454a1a20d2ed4ae5ab89355c83920f46ee2de4e14c0746d44ed6f80f584fcc9555ed63ff00a6ab788e6652d17f064761f01fb15c9ba4c264a5c32164bc3c7217d459ae0e01b2b8b9a2e3227848bd953dbe0c224a5c4a494bd85b547a445c0ebbd8035ad21ede59836e447bd71e78f7e371fcbeae939fd3f3e1cbadf6d95a117ccc37166c9d57d9b272fb2ef2ee3e0a5575732219e6e3a346a7ee0ba6bc39ccbb35eef4ce3fd4ba6cf83d44ce764f3f5f5afcfd7ca1ed111c0d1f5b8ee3c8037f985d79daa935552e91dc4e39e800d00ee0a2b755dc7071de3c2637cbcebf55eb31eafaacb9719ac7c4fe992e51172bae0a8b26aa539459b272094cd1683938f8e6b6b4ad751c8f8a0d8731e0afedcdedf74b60a2ab7deb6165e191c73a985bde79c8d1af78cfbd79fd8577bdd8ec556d64f1d4c2e34d4d4f2b64e96466e731d9b226fd739104f645c837d1291e964445968444404444044441586f0775704ed7d461d1886b6c5e60670b60a83cc007263cf222c09d75b8a1eb227c6e732463a39184b1ec7b4b5ec70e4e0745ec75d2778bbbd8314671b3861c418db473dbaaf03f27281da6f71d472e60d952c7981da2dccec0ff00ee6b6e2b86cd4d2be0a88dd14f13b85ec7723c883cda750464415aa3ec0551a8eaa5c47aaa2152a9b441aa653f01a7865a8863a99248e9e591b1c9244d6ba46f164d203b2ed16dfb85f23a28150be8ece523e6aaa78e2639ef7544566b1a5c6c2405c6c390009279004a0b4b1bdde5161dea98fc63148c543dcc861a78dd217380e2759910f1be8ba0edee0d0524ace8b59d320a8a66d4b6671699097170b3adec8d73cedc95f5b7bb40da07d24f2d189e99b24a26a810fac96938a3e1618dda30b89e137d464a98ddc6ce9c43106c8e84f438653555043498ee1dc6c8af6b12496e5af082a45afafb55ba434b43d2a9e79669a28db2d544f6b40e0b02f7476171c3ad893903eff83b03b2b1624ea996aeadd4f4b470b659a51c3c777f1f0e6e0406811bc9cbb95d7b138d52554b56c86b6a6acbe532c915453cd1b2981ea189a5ec000c80e139e44f7aa276df656a28ab25a48a29dd1ccf3d0dac6c8ee9111eb31ad03fac2cb869f16df9a2efdb5f0b126dcfe1d1b63925c56a1b0ccf8e38dc5b0b78dd21b31a0f0e44dc2ab76bb02e8159352f1fac6c4e1c0f360e731ec0f6f101a3aceb1f25786f7b0e94e0a191c6f7ba0303a40c05c5b1c62ce710390d49e42e579dc3c924b897389b97389249f12754895905cae02c82a8c5ca3556a3c94976aa3d5f2f7a0dac3a7924cdb8b004926c00cc93c96cc3e9649a46450c6e96690f0c71b05dce3e03f6f85ae57a17765bb46505aa2b0325c408ea01d68e941e4c3f59fdeff70e65c34ea7bb7dd0ba40da8c55ae64793a3a2ecbde3919f9b47e60cfbfb95df042d6343236b591b006b18c01ad6b468001900b622cb42222022220222202222022220e9fbc0d80a7c55ac2e7fa8a989c386a18c0e7186fd68dc2e2e398ee3e641a3b7a3b3d061d56da7a60ff005429a290991e5ef7c85d207389d05f8464001dc17a8579df7fedb624df1a284ff9b38fe0ac4aad5ead5d97dd6c15740dac8f12792e89cf731b4fd5648cbf14762ee2241045f9ea35555bb4f72b87d1e71de17cf44f39483a5403f3859928f87ab3ee72b51028f75b4b51878ae8f1395ec740e9ad1d30203980f1b384bb88905a47b97c9a5d9a6418753e274b88d436ba691b0d3431c258e7d4b9c58f8a37037d03fada1b5b9ab8287682923ad9709a78991b69a9c4cc0dec995cf2f95807781246ef7bbb957fb658fd3418bd053b1ac8f0ec2a4671b1b9471cb2b839eeb7e602c779f128afa72ec5d54ac8a0c6768e564f567e8a8b8c39ae7b6c786ee204841b72b5ed6beabae62bb3d8860d510c1fcab35361b59358d6538786b5f6b75e20727d8345ef9817faa40ee7bead98a9ab6d3555046e9a780b9b68882fe17f0be391bdfc2e60d3ed5f92d9beaac61a5a4a67d8d6d4d640591b6c5cde1367b8785ddc3fa483a96d9ec957607174aa2c52adf1cd270d63efc0e0f7125923ec4875c970b9ceee1dea4cdb13552d03713c4f18ab8aa2280d4c41cd7bdd4ed3d660043839af3d5bf0d8dec392b364c629e7a8aca1ab8e331d3c31cee128bb25a57b389ce20e4435e0827c97c4da8c4dd886cfcf50d85ccf5d03e4647625dea5b3dda4f9b1a1def4d8eb755813e5c37a5d4ed4571c39f1074b781f62d73830b5cd0ee23d63c365d2f11d91c3228e09598bbfd4c957d16a4cd4ce8e581a627481fea4d9f6b346672eb83cb3b2b675859b32c2fa36d6da17cc295ed2e6cad352e91990049b02d70b77055dedee11515efaac4a2a5920a6069a9618a68a48ea6a64735b1fd1c76bbace207881969601f476cf7433d1c3eba8e57d6318099a33186ccd6fda606f6c778d7cd7cca9d8ea36612cc45b88bcba5018c84c166baab3e2841bdc58b1fd6d2cdbab736976ec61b5b053d5c24504d4ed774c01c7d5cfc6e6b81e45a006136cc715f35d7f7e5142dc329cd3b6210bf116cad308688de64a7a87178e1c8f1124df9dd3669459d5764d87d8c38b4b344d9bd4be1a712b1e5bc4c2f3235bc2e1adadc5a73b2eb67556cfa3c37f09ac3dd0423e2f7fdcad48b1f60b60e970a8fe8fe96ade2d3553da03ddf9ac1f5197e5f12576c4459684444044440444404444044440444405e7cf4856ff004844791a18c7c279fef0bd06a85f48a67e174c799a670f84a7fdc55895541d14dc1aba5a7919353c8e8a78c931c8db7134905a75c8dc122c7bd4190e4b741a0551326c5aa193f4964f236af8dd219c1eb97bafc44f2cee72d33511d33a425f238be47b8bdef71bb9cf7125c49ef2495c5668b5c07241d8707db0c4a95822a6af9e38464d8eec91ac1dcd0f0784780b2f9f3635542a1b53d266358d3c4da873cba506c4644f2b122da58a88d5ae7d507d5c4768eb6a5dc75157348f313a024bb86f0bbb51d9b61c2798e6a647b6f8a36210b710a810067ab0cea5c46058378b878b4cb55d798b2083b20dbac59a2cdc4aa4340000bb32034e4a054ed86253707adafa87fa9944f112f00b256820381035009f0ccaf98ed146620fb58d6d1d6d6f08acaa96711dcb03f8435a4e4480d005fc56976253ba0653ba679a58e432c701378d92104173472ed3b2d333dea085984189d55c1e8ecdfa4ae3dcca61f174ff0072a7b9ab8fd1d7b75decd2fcea1291752222cb42222022220222202222022220222202a23d22bf19a5ff000f27ef02bdd50fe911f8d537f8677ef5589551c8a54634511faa9839792a8c2af45a612b7d568a3c4824b56b9d6c62d736a80d592c58b308129c9478d6f996866a837b564162164106bbe6ae3f474edd7fb34bf3a854d8d55c9e8e7dbaff006697e750948bad11165a1111011110111101111011110111101515e9103f09a5ff000f27ef1aaf55467a440fc2293fec4dfeb67deac4aa70ea14e1a050398539ba2a8e27d145854a97451234129ab09d671ac2740668b362d6d5b5883195478b552255a29f52837acb92c166506a6ab93d1c9dd6af1e14a7c7f2ea9a6ab8fd1c4f5ebfd9a6f9ce9562ed4445951111011110111101111011110111101525e912dfa5a23fdd540f83a1fbd5daa95f489edd0fb155f3a748552475f7a9cc509ddaf7a98dd5699732e8a18d54b9745139a09312c675cc49320c42dad5a5ab68418cda2d34fcd6d9f45a6041bda164e28c58bca0d6d570fa388fa4aef629be732a782b8fd1bfb75fecd37ce74ab1772222ca8888808888088880888808888088880a9af48867e24ee63a437e3ea4ff000572aa83d21c7d1519fef651f1637ee5625510eed7bd4c0a1cbafbd4c8d542639288a4d468b420db1aca458b164ed106a8d6e0b4c6b7041aea745aa9d67547258d3e88243560f59ac1e835ab93d1bfb75fecd2fce754d5d5cde8dfdaaff6697e750a558bb5111451111011110111101111011110111101567befc0eaeae2a61494f24ee8e67b9e2302ed059604dcab311079464ddde3273fe4ca8ff2ff00dcb6b3613161ae1955fa80fc8af54a2bb4d3cb3fcde630fd30c9ff0048c2dff53c2d8ddd6637fd9e479d452dff0078bd4489b34f31ff003578d017e817f2a8a5bfef16a76edb1afecd97ff002d37fc8bd4289b34f2d47bb3c6bfb364f7cb4c3e7229b1eeb31a3ff42079d4530ffdd7a6113669e66937478d38dba2c6077baa20b7ec712a543b98c600d290781a875ff6317a3d13669e766ee67173af421e75127f08d6677278b5bfada0f2f5f3ff00c4bd0c89b34f38c9b94c5f91a23e53c9fc630ac5dceec4d5e19d24d67aa067f5218227f1e51facb9390fb615928a2888880888808888088880888808888088880888808888088880888808888088880888808888088880888808888088883fffd9, 5, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rango`
--

CREATE TABLE `rango` (
  `id_rango` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rango`
--

INSERT INTO `rango` (`id_rango`, `nombre`) VALUES
(1, 'Administrador'),
(2, 'Cliente'),
(3, 'Vendedor'),
(4, 'Cobrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT 1,
  `id_rango` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `contraseña`, `estado`, `id_rango`) VALUES
(1, 'Admin', NULL, 'Admin@gmail.com', '1234', 1, 1),
(2, 'Jairick', NULL, 'Jairosebastian@gmail.com', '12345678', 1, 2),
(3, 'Nestor ', NULL, 'Nestor@gmail.com', '12345678', 1, 3),
(4, 'Omar Enrique', NULL, 'omar@gmail.com', '12345678', 1, 4),
(5, 'Omar', NULL, 'omarenrique108@gmail.com', '12345678', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vendedor`
--

CREATE TABLE `vendedor` (
  `id_vende` int(11) NOT NULL,
  `nombre` varchar(20) DEFAULT NULL,
  `apellido` varchar(20) DEFAULT NULL,
  `tel` varchar(15) DEFAULT NULL,
  `id_rango` int(11) DEFAULT NULL,
  `id_zona` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vendedor`
--

INSERT INTO `vendedor` (`id_vende`, `nombre`, `apellido`, `tel`, `id_rango`, `id_zona`) VALUES
(1, 'Nestor ', 'Ramirez', '23232323', 3, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `zona`
--

CREATE TABLE `zona` (
  `id_zona` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `zona`
--

INSERT INTO `zona` (`id_zona`, `nombre`) VALUES
(1, 'Centro'),
(2, 'Norte'),
(3, 'Sur'),
(4, 'Este'),
(5, 'Oeste');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `abono_venta`
--
ALTER TABLE `abono_venta`
  ADD PRIMARY KEY (`id_abono`),
  ADD KEY `id_factura_venta` (`id_factura_venta`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_cobrador` (`id_cobrador`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `tel` (`tel`),
  ADD UNIQUE KEY `dui` (`dui`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_rango` (`id_rango`);

--
-- Indices de la tabla `cobrador`
--
ALTER TABLE `cobrador`
  ADD PRIMARY KEY (`id_cobrador`),
  ADD UNIQUE KEY `tel` (`tel`),
  ADD KEY `id_rango` (`id_rango`),
  ADD KEY `id_zona` (`id_zona`);

--
-- Indices de la tabla `cobrador_cliente`
--
ALTER TABLE `cobrador_cliente`
  ADD PRIMARY KEY (`id_cobrador`,`id_cliente`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indices de la tabla `contrato`
--
ALTER TABLE `contrato`
  ADD PRIMARY KEY (`id_contrato`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_vende` (`id_vende`),
  ADD KEY `id_cobrador` (`id_cobrador`);

--
-- Indices de la tabla `factura_cobro`
--
ALTER TABLE `factura_cobro`
  ADD PRIMARY KEY (`id_factura_cobro`),
  ADD KEY `id_cobrador` (`id_cobrador`),
  ADD KEY `id_zona` (`id_zona`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indices de la tabla `factura_venta`
--
ALTER TABLE `factura_venta`
  ADD PRIMARY KEY (`id_factura_venta`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_vende` (`id_vende`),
  ADD KEY `id_product` (`id_product`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_product`),
  ADD KEY `id_catego` (`id_catego`);

--
-- Indices de la tabla `rango`
--
ALTER TABLE `rango`
  ADD PRIMARY KEY (`id_rango`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_rango` (`id_rango`);

--
-- Indices de la tabla `vendedor`
--
ALTER TABLE `vendedor`
  ADD PRIMARY KEY (`id_vende`),
  ADD UNIQUE KEY `tel` (`tel`),
  ADD KEY `id_rango` (`id_rango`),
  ADD KEY `id_zona` (`id_zona`);

--
-- Indices de la tabla `zona`
--
ALTER TABLE `zona`
  ADD PRIMARY KEY (`id_zona`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `abono_venta`
--
ALTER TABLE `abono_venta`
  MODIFY `id_abono` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cobrador`
--
ALTER TABLE `cobrador`
  MODIFY `id_cobrador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `contrato`
--
ALTER TABLE `contrato`
  MODIFY `id_contrato` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `factura_cobro`
--
ALTER TABLE `factura_cobro`
  MODIFY `id_factura_cobro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `factura_venta`
--
ALTER TABLE `factura_venta`
  MODIFY `id_factura_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `rango`
--
ALTER TABLE `rango`
  MODIFY `id_rango` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `vendedor`
--
ALTER TABLE `vendedor`
  MODIFY `id_vende` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `zona`
--
ALTER TABLE `zona`
  MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `abono_venta`
--
ALTER TABLE `abono_venta`
  ADD CONSTRAINT `abono_venta_ibfk_1` FOREIGN KEY (`id_factura_venta`) REFERENCES `factura_venta` (`id_factura_venta`),
  ADD CONSTRAINT `abono_venta_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `abono_venta_ibfk_3` FOREIGN KEY (`id_cobrador`) REFERENCES `cobrador` (`id_cobrador`);

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`id_rango`) REFERENCES `rango` (`id_rango`);

--
-- Filtros para la tabla `cobrador`
--
ALTER TABLE `cobrador`
  ADD CONSTRAINT `cobrador_ibfk_1` FOREIGN KEY (`id_rango`) REFERENCES `rango` (`id_rango`),
  ADD CONSTRAINT `cobrador_ibfk_2` FOREIGN KEY (`id_zona`) REFERENCES `zona` (`id_zona`);

--
-- Filtros para la tabla `cobrador_cliente`
--
ALTER TABLE `cobrador_cliente`
  ADD CONSTRAINT `cobrador_cliente_ibfk_1` FOREIGN KEY (`id_cobrador`) REFERENCES `cobrador` (`id_cobrador`),
  ADD CONSTRAINT `cobrador_cliente_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`);

--
-- Filtros para la tabla `contrato`
--
ALTER TABLE `contrato`
  ADD CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `contrato_ibfk_2` FOREIGN KEY (`id_vende`) REFERENCES `vendedor` (`id_vende`),
  ADD CONSTRAINT `contrato_ibfk_3` FOREIGN KEY (`id_cobrador`) REFERENCES `cobrador` (`id_cobrador`);

--
-- Filtros para la tabla `factura_cobro`
--
ALTER TABLE `factura_cobro`
  ADD CONSTRAINT `factura_cobro_ibfk_1` FOREIGN KEY (`id_cobrador`) REFERENCES `cobrador` (`id_cobrador`),
  ADD CONSTRAINT `factura_cobro_ibfk_2` FOREIGN KEY (`id_zona`) REFERENCES `zona` (`id_zona`),
  ADD CONSTRAINT `factura_cobro_ibfk_3` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`);

--
-- Filtros para la tabla `factura_venta`
--
ALTER TABLE `factura_venta`
  ADD CONSTRAINT `factura_venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `factura_venta_ibfk_2` FOREIGN KEY (`id_vende`) REFERENCES `vendedor` (`id_vende`),
  ADD CONSTRAINT `factura_venta_ibfk_3` FOREIGN KEY (`id_product`) REFERENCES `producto` (`id_product`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`id_catego`) REFERENCES `categoria` (`id_categoria`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rango`) REFERENCES `rango` (`id_rango`);

--
-- Filtros para la tabla `vendedor`
--
ALTER TABLE `vendedor`
  ADD CONSTRAINT `vendedor_ibfk_1` FOREIGN KEY (`id_rango`) REFERENCES `rango` (`id_rango`),
  ADD CONSTRAINT `vendedor_ibfk_2` FOREIGN KEY (`id_zona`) REFERENCES `zona` (`id_zona`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
