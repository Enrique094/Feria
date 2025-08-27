-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-08-2025 a las 01:39:08
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
  `Cuotas` bit(1) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `interes_aplicado` decimal(5,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `es_credito` decimal(10,0) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `factura_venta`
--

INSERT INTO `factura_venta` (`id_factura_venta`, `id_cliente`, `id_vende`, `id_product`, `fecha`, `hora`, `Precio_Mensual`, `Cuotas`, `direccion`, `interes_aplicado`, `total`, `es_credito`) VALUES
(4, 1, 1, 3, '2025-08-27', '17:15:38', 4, b'1', 'Santa Teresa de las flores :D', 8.00, 26.99, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intereses`
--

CREATE TABLE `intereses` (
  `id` int(11) NOT NULL,
  `meses` int(11) NOT NULL,
  `porcentaje` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `intereses`
--

INSERT INTO `intereses` (`id`, `meses`, `porcentaje`) VALUES
(4, 3, 5.00),
(5, 6, 8.00),
(6, 12, 12.00),
(7, 18, 15.00),
(8, 24, 18.00);

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
  `imagen_blob` mediumblob DEFAULT NULL,
  `stock` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_product`, `id_catego`, `nombre`, `descripcion`, `precio`, `imagen`, `imagen_blob`, `stock`) VALUES
(3, 1, 'Camisa', 'Camisa con estampado para Hombre', 24.99, 1, 0xffd8ffe000104a46494600010100000100010000ffdb00840009060710111215130f0e0f100d1010150f0f0f0f1010100f100f1512171715151515181d2820181a261d15152131212629372e3232171f333835354328392f2b010a0a0a0e0d0e170f10172d1d151d2d2d2e2e2d2e2b2d2b372d2d372d37373737342b2b372d2e37372d2f2b2d3737303732372b2b2b2c2d2b37322d3737372d31ffc000110800d900e803012200021101031101ffc4001c0001000202030100000000000000000000000407020301060805ffc4004910000103020304060604090b0500000000010002030411052131060712411422325161710813728191b1234252d1243443628292a1b3c115172533556374a3b2d2d3447393c2f0ffc4001a010101010003010000000000000000000000010203050704ffc4002511010100020103040105000000000000000001021103041231142141615105131581b1ffda000c03010002110311003f00bc511101111011110111101111011145c4311829dbc7513c5047f6e691b1b7e2e282522e975fbd4c1627861ae6c879ba08e5998d1e2e63483eebafaf86ed961951fd4e214af27ea9998c7fea38823e083eea2c6391ae176b83877820851eb71182104cf3c31346a65918c03e2504a45d2f10dea60d0b834d70909362608e5998d1de5cc691f0375d8307da3a2abfc56b29e736b96c7235cf03c59a8f7841f511110111101111011110111101111011110111101111011155bb5fbe4a7a67be1a287a54cc25a6673b86943c646c46725bc2c3c505a4baa6d36f0f0ca0bb65a91254375a7a7fa5981ee701930fb442a1b1edbfc52b2e25ac7b223f91a6fa08edddd5eb387b4e2bab0681a0b2ba4daceda3df4574d76d144ca38b301eeb4d50477e7d46f958f9aadf11ad9aa1e64a99a49e53f9499ee7bad7d013a0f0192d375c2a8d03b5fa2b6165fb8f98584a3470e5af92d80a0e1adb7672f2cbe4b1f563b87c16d5c1418596701b105a4b5edb16b9a4b5cd23982330562e2b96a0eeb816f4b17a4b03502aa21f52ada6436f09059f7f32558d80efbe8a4b36b29e6a47f37b7f0886fe6d01e3f57dea8725604268dbd7f83e3d4956de2a4aa8671cfd548d739bed37569f0217d15e3089ce6383d8e732469bb5ec716bda7bc38661583b25bdeafa5735b56e35b4b701dc7c22a58def6499711f076bde14d2ede8e45130ac462a98639e0787c13303e378b8bb4f783983c883a594b5144444044440444404444044440445f2b6a31d8a82965a99bb3137aade724872630789240fda82b8df6edbbe11d0295fc324ad06ae46921cc89dd989a4685c2e4f85bed65468eeeec87c4a998a57495133e699dc534af74d21e5c4e3a0ee02f60390002872647e1fc5699640a15cae0a0c51172107042c032da69ddf72dab8b20c2eb82f593dab0b20e005b170b241c22e57050160751e6b35aa4398f6bee416dee2b6c3d4ccec3e77fd0cee2fa52e3932723ad1f8070171f9c0f372be578bc3cb5e1cd716b8105ae69b39ae69b820f220e6bd3fbb1db1189d282f2d15b05a3a960cae6dd5940fb2e009f021c3929563b8a2228a222202222022220222202f3a6f776c7a7d57a885d7a1a4710d2349a7170f93c40cdadfd23cd77ddf3edb7458ba1d3bad5750cfa57b4e70539c8f93dd981dc2e7baf4242323f01e4ac4ad529ed7b3fc56329b8bf805c4e723e2570dec0551b5a742b9705ae1397915b8e8835ae42c5737b0fda8325cab4307dcad4cd132476214ac12303da228df50db1171d7e2683ee5d4f6cb63e5c3aa194e6a21a87c8ce31eaaed7b05ff0028c24f05f506f9d8f726e2e38dcac926ed75972c17d77e0525ae1ec2efb39dbe2b5d2e0b23c5c90cee04127dfdcb87d4716b7dcec7f87ebbba61fb5777dfe3fdf0f9a172a455d1be23675b3d1c342a3b972e394ca6e787c1cbc59f16770ce6b29e6570b92810aac0028f21cdbe67e6a428d26a106d9f91eeb2ec1b15b4d261d54ca88eee60ea4f1036f5b01ed37cc6447880be13c5dbee5ae177dc83d9586d7c551132681e1f0cac1246f1a169171e47c149540ee5b6dba2ca28aa5f6a4a87fd03dc7286a1df57c1af3f077b455fcb2d0888808888088880be36d6ed14387533ea26cc3470c718ed4b29ecb1be7dfc802792fb2a91dfae1189c9289f80cb8642c0231092e30b88fa47cacd6e4fd6170001a730aab16c465aa9a49a77714f33cbe4772b9e40726816007700b0b5805aa1175b1e755a650e6ecfbd731f6079958bfb3ef59b075020e213aa93c9456e454a1a20d2ed4ae5ab89355c83920f46ee2de4e14c0746d44ed6f80f584fcc9555ed63ff00a6ab788e6652d17f064761f01fb15c9ba4c264a5c32164bc3c7217d459ae0e01b2b8b9a2e3227848bd953dbe0c224a5c4a494bd85b547a445c0ebbd8035ad21ede59836e447bd71e78f7e371fcbeae939fd3f3e1cbadf6d95a117ccc37166c9d57d9b272fb2ef2ee3e0a5575732219e6e3a346a7ee0ba6bc39ccbb35eef4ce3fd4ba6cf83d44ce764f3f5f5afcfd7ca1ed111c0d1f5b8ee3c8037f985d79daa935552e91dc4e39e800d00ee0a2b755dc7071de3c2637cbcebf55eb31eafaacb9719ac7c4fe992e51172bae0a8b26aa539459b272094cd1683938f8e6b6b4ad751c8f8a0d8731e0afedcdedf74b60a2ab7deb6165e191c73a985bde79c8d1af78cfbd79fd8577bdd8ec556d64f1d4c2e34d4d4f2b64e96466e731d9b226fd739104f645c837d1291e964445968444404444044441586f0775704ed7d461d1886b6c5e60670b60a83cc007263cf222c09d75b8a1eb227c6e732463a39184b1ec7b4b5ec70e4e0745ec75d2778bbbd8314671b3861c418db473dbaaf03f27281da6f71d472e60d952c7981da2dccec0ff00ee6b6e2b86cd4d2be0a88dd14f13b85ec7723c883cda750464415aa3ec0551a8eaa5c47aaa2152a9b441aa653f01a7865a8863a99248e9e591b1c9244d6ba46f164d203b2ed16dfb85f23a28150be8ece523e6aaa78e2639ef7544566b1a5c6c2405c6c390009279004a0b4b1bdde5161dea98fc63148c543dcc861a78dd217380e2759910f1be8ba0edee0d0524ace8b59d320a8a66d4b6671699097170b3adec8d73cedc95f5b7bb40da07d24f2d189e99b24a26a810fac96938a3e1618dda30b89e137d464a98ddc6ce9c43106c8e84f438653555043498ee1dc6c8af6b12496e5af082a45afafb55ba434b43d2a9e79669a28db2d544f6b40e0b02f7476171c3ad893903eff83b03b2b1624ea996aeadd4f4b470b659a51c3c777f1f0e6e0406811bc9cbb95d7b138d52554b56c86b6a6acbe532c915453cd1b2981ea189a5ec000c80e139e44f7aa276df656a28ab25a48a29dd1ccf3d0dac6c8ee9111eb31ad03fac2cb869f16df9a2efdb5f0b126dcfe1d1b63925c56a1b0ccf8e38dc5b0b78dd21b31a0f0e44dc2ab76bb02e8159352f1fac6c4e1c0f360e731ec0f6f101a3aceb1f25786f7b0e94e0a191c6f7ba0303a40c05c5b1c62ce710390d49e42e579dc3c924b897389b97389249f12754895905cae02c82a8c5ca3556a3c94976aa3d5f2f7a0dac3a7924cdb8b004926c00cc93c96cc3e9649a46450c6e96690f0c71b05dce3e03f6f85ae57a17765bb46505aa2b0325c408ea01d68e941e4c3f59fdeff70e65c34ea7bb7dd0ba40da8c55ae64793a3a2ecbde3919f9b47e60cfbfb95df042d6343236b591b006b18c01ad6b468001900b622cb42222022220222202222022220e9fbc0d80a7c55ac2e7fa8a989c386a18c0e7186fd68dc2e2e398ee3e641a3b7a3b3d061d56da7a60ff005429a290991e5ef7c85d207389d05f8464001dc17a8579df7fedb624df1a284ff9b38fe0ac4aad5ead5d97dd6c15740dac8f12792e89cf731b4fd5648cbf14762ee2241045f9ea35555bb4f72b87d1e71de17cf44f39483a5403f3859928f87ab3ee72b51028f75b4b51878ae8f1395ec740e9ad1d30203980f1b384bb88905a47b97c9a5d9a6418753e274b88d436ba691b0d3431c258e7d4b9c58f8a37037d03fada1b5b9ab8287682923ad9709a78991b69a9c4cc0dec995cf2f95807781246ef7bbb957fb658fd3418bd053b1ac8f0ec2a4671b1b9471cb2b839eeb7e602c779f128afa72ec5d54ac8a0c6768e564f567e8a8b8c39ae7b6c786ee204841b72b5ed6beabae62bb3d8860d510c1fcab35361b59358d6538786b5f6b75e20727d8345ef9817faa40ee7bead98a9ab6d3555046e9a780b9b68882fe17f0be391bdfc2e60d3ed5f92d9beaac61a5a4a67d8d6d4d640591b6c5cde1367b8785ddc3fa483a96d9ec957607174aa2c52adf1cd270d63efc0e0f7125923ec4875c970b9ceee1dea4cdb13552d03713c4f18ab8aa2280d4c41cd7bdd4ed3d660043839af3d5bf0d8dec392b364c629e7a8aca1ab8e331d3c31cee128bb25a57b389ce20e4435e0827c97c4da8c4dd886cfcf50d85ccf5d03e4647625dea5b3dda4f9b1a1def4d8eb755813e5c37a5d4ed4571c39f1074b781f62d73830b5cd0ee23d63c365d2f11d91c3228e09598bbfd4c957d16a4cd4ce8e581a627481fea4d9f6b346672eb83cb3b2b675859b32c2fa36d6da17cc295ed2e6cad352e91990049b02d70b77055dedee11515efaac4a2a5920a6069a9618a68a48ea6a64735b1fd1c76bbace207881969601f476cf7433d1c3eba8e57d6318099a33186ccd6fda606f6c778d7cd7cca9d8ea36612cc45b88bcba5018c84c166baab3e2841bdc58b1fd6d2cdbab736976ec61b5b053d5c24504d4ed774c01c7d5cfc6e6b81e45a006136cc715f35d7f7e5142dc329cd3b6210bf116cad308688de64a7a87178e1c8f1124df9dd3669459d5764d87d8c38b4b344d9bd4be1a712b1e5bc4c2f3235bc2e1adadc5a73b2eb67556cfa3c37f09ac3dd0423e2f7fdcad48b1f60b60e970a8fe8fe96ade2d3553da03ddf9ac1f5197e5f12576c4459684444044440444404444044440444405e7cf4856ff004844791a18c7c279fef0bd06a85f48a67e174c799a670f84a7fdc55895541d14dc1aba5a7919353c8e8a78c931c8db7134905a75c8dc122c7bd4190e4b741a0551326c5aa193f4964f236af8dd219c1eb97bafc44f2cee72d33511d33a425f238be47b8bdef71bb9cf7125c49ef2495c5668b5c07241d8707db0c4a95822a6af9e38464d8eec91ac1dcd0f0784780b2f9f3635542a1b53d266358d3c4da873cba506c4644f2b122da58a88d5ae7d507d5c4768eb6a5dc75157348f313a024bb86f0bbb51d9b61c2798e6a647b6f8a36210b710a810067ab0cea5c46058378b878b4cb55d798b2083b20dbac59a2cdc4aa4340000bb32034e4a054ed86253707adafa87fa9944f112f00b256820381035009f0ccaf98ed146620fb58d6d1d6d6f08acaa96711dcb03f8435a4e4480d005fc56976253ba0653ba679a58e432c701378d92104173472ed3b2d333dea085984189d55c1e8ecdfa4ae3dcca61f174ff0072a7b9ab8fd1d7b75decd2fcea1291752222cb42222022220222202222022220222202a23d22bf19a5ff000f27ef02bdd50fe911f8d537f8677ef5589551c8a54634511faa9839792a8c2af45a612b7d568a3c4824b56b9d6c62d736a80d592c58b308129c9478d6f996866a837b564162164106bbe6ae3f474edd7fb34bf3a854d8d55c9e8e7dbaff006697e750948bad11165a1111011110111101111011110111101515e9103f09a5ff000f27ef1aaf55467a440fc2293fec4dfeb67deac4aa70ea14e1a050398539ba2a8e27d145854a97451234129ab09d671ac2740668b362d6d5b5883195478b552255a29f52837acb92c166506a6ab93d1c9dd6af1e14a7c7f2ea9a6ab8fd1c4f5ebfd9a6f9ce9562ed4445951111011110111101111011110111101525e912dfa5a23fdd540f83a1fbd5daa95f489edd0fb155f3a748552475f7a9cc509ddaf7a98dd5699732e8a18d54b9745139a09312c675cc49320c42dad5a5ab68418cda2d34fcd6d9f45a6041bda164e28c58bca0d6d570fa388fa4aef629be732a782b8fd1bfb75fecd37ce74ab1772222ca8888808888088880888808888088880a9af48867e24ee63a437e3ea4ff000572aa83d21c7d1519fef651f1637ee5625510eed7bd4c0a1cbafbd4c8d542639288a4d468b420db1aca458b164ed106a8d6e0b4c6b7041aea745aa9d67547258d3e88243560f59ac1e835ab93d1bfb75fecd2fce754d5d5cde8dfdaaff6697e750a558bb5111451111011110111101111011110111101567befc0eaeae2a61494f24ee8e67b9e2302ed059604dcab311079464ddde3273fe4ca8ff2ff00dcb6b3613161ae1955fa80fc8af54a2bb4d3cb3fcde630fd30c9ff0048c2dff53c2d8ddd6637fd9e479d452dff0078bd4489b34f31ff003578d017e817f2a8a5bfef16a76edb1afecd97ff002d37fc8bd4289b34f2d47bb3c6bfb364f7cb4c3e7229b1eeb31a3ff42079d4530ffdd7a6113669e66937478d38dba2c6077baa20b7ec712a543b98c600d290781a875ff6317a3d13669e766ee67173af421e75127f08d6677278b5bfada0f2f5f3ff00c4bd0c89b34f38c9b94c5f91a23e53c9fc630ac5dceec4d5e19d24d67aa067f5218227f1e51facb9390fb615928a2888880888808888088880888808888088880888808888088880888808888088880888808888088880888808888088883fffd9, 2),
(4, 2, 'Lavadora', 'Tecnología Aqua Saver Green optimiza el consumo para ahorrar más agua y energía por lavada.', 499.99, 1, 0xffd8ffe000104a46494600010100000100010000ffdb0084000906070f0f100f0f100e100f0f0f100d0e0f0f100f10100f0d0f1511181616111615181e2820181d251b151521312125292b2e2e2e171f3338332d37282d2e2b010a0a0a0d0d0d0e0d0d152b1915192b2e2b2d2b2d2b2d322b2b2b2b2b2b2b372d2b2b2b2b2d2b2b2d2b2b2b2d2b372b2b372b2b2d372b2b2b2b2b2b2b2b2d2b2bffc000110800e100e103012200021101031101ffc4001c0001000202030100000000000000000000000102050703060804ffc4004a100002010202030a09070b0305000000000001020311040512213106071341515261718191229293a1b1c1d1d2e11432535462a2c2151623424463728283b2f043a3c317246473e2ffc4001501010100000000000000000000000000000001ffc400161101010100000000000000000000000000001101ffda000c03010002110311003f00de200000000000000000e1c662a9d1a73ab566a9d3a71729ce4eca3146b5cc37f0cb294e508d1c4d451d5a6a108a7d366eebb52606d006a57bfbe038b0b5fb5c5133dfcf0895fe455edcae692fed036c83504b7f9c22fd8aaf47e957ba16ff001857abe4356ef62e135bfb806df06a49efe1423ade5f56db6fc345f7da3a8e2ffaf585fa8d5f2abdd037003502dfeb07c782ade517ba5d6ff181e3c257f197b00db80d4cb7f7cbf8f0d88ecd1666373bbeee598da8a97e970f26d252ab18e85dead6d3d5d6d5ba40d820000000000000000000000000000000001d1b7d5dd1d4c261e9d1a1370af8972f0e2ed3a7463f39a7c4db7157ebb6c03adefe9ba850a70c0d29c5b57ad8951927a2d6aa54a5d6db95b6ea8f29e7d6efadeb6f5be96761ceeac5b50937e15e527c6ddffc662781a5ce97f9d815c5824e538c6eece5ad2766d71a5d88fba8d06d2bd47769cf549dad1564b674d8f925469f149f6a28e947957732447d9982a94e34de9c1c6a4362579c17366dc559f51ccabf06ef28c65171941daca6aeb6c6e7c13bcaca52ba5a95dc9d97415946fb657ebd2655dd64696329c5e9454e52d71519c21186b4d3bf84eeb5bd5a8f8b1f051d0e571d768a8ebecda71bbbb5e57b6a5f3b52e81257db2bdb65f49d80a519454939c5ca17f0a3196849ae8959dbb8fb655705a3aa86274afaff004f4ed157e2f035f16d3e4e0d72aee61538f2aee6070b576ec9db5d96d691f5e1a9d5a0e159c24a1e0bd2b5e2e32e2b958c62bf59aeaba26518bdb293eb7708f51ef5bba358dc142129a788c37e8a69bf0e54d5b42a5b6b5a2d2bf1b8b3b91e50dcae673a528ca954942a41a519c5da4acb579b5749e94dc7677f2ec253acedc22bd3ac971558edd5c574d4adc924066c0000000000000000000000000000d07be466df29c762249de147feda9f541b52fbee6fb8dd7ba3cc96130988c43db4a94e51bf1d4b5a0bb64d2ed3cd38ba8ecdb777ae4df1b7b6e0759cd277a8fb8fb72cc9e35637729294a2e504aca32b713d462f152f0a5d0769c3c1c234d2d4e11859f4a4061ff27c2f6b3ef64bcb63b6cfbd99fc4d2535c34756c5517365cbd4cf9dbbeae2030eb2d4ff0055f8df11f935735f7fc4cc5183d9e0db8f49b56ee4ce3ab56716d68464b954ee9f980c57e4e5cd7dff0011f937ecbeff008990f944fe8beffc0e6a35273d5a318f5cff00f903112cbd2fd57e37c4a4b02b91f7b3275af7b6abdd6cd9b4aca6f8ecc0c64300a4d455f5f4ec387198654df82db8ddabbb7a8cdcd682fb72fbb131f9843c0bf234fd5eb038f27a9a33ff0036ff00891ba77a1ce383c4cf0d27e062a1a505fbd826f575c74bc5468ec1ced25dfdc776c931f2a13a35e1f3e8d48548ebb5f4649e8f535abb40f4d838b0b888d5a70ab077854846a41f2c64ae9f733940000000000000000000000000d7dbf3663c1e128e1d3d788aba525cb4e9abff00738771a471f3b45f57a59b037decc785cc3824fc1c352a74edf6e5e1c9f74a0bb0d6d9bced0975a5e60309421a75211b7cf9c53ea72d676faba8eb79052d2c4535c9a52ebb459de30b9770ad5d6a5afb40c0d49cdea84252ead51ef38ff4ebfd07defd876a9e269536e9d1a4f11563aa4a3654e9bfb737aa3d5b7a0e1af0c4d45e1d68518f3284349f539cbd48b06029d5a9f45257dbad35e7386be2745eb8be8f99ed32d3caa9bf9cea547f6ea49fa2c71d6ca6968db81bf4284a6ee0623e5d1e4fecf68f963e283ecd0f696ab97538bb701fed3f610b2ca4f5f036ec941fa80e0955a8f6526ddf6b7ec21badf44fbfe07d94f0097cca9569f54f49774ae7d31ab88871d3c44791ae0aa7bafcc06314f65d38be47c7da2b474a125cb17de65a12a35ef0b3a7512d74e6b464ba7a5749f34f0ae0ecf65f57b00eb34dd9a7d276bcae778f627ea3aa548da525c8daee6760c96a5d47a5497ac83d0dbd5e65c3e5f083779e1a73a0ff0087e743b346497f29dc0d3fbcee61a18bad876f56229292ff00d949dd25fcb39f8a6e000000000000000000000004376d6498bdd5625d1c0e36aad4e9e171334f91aa526079e73dc7fca71589af7bf0b5aacd7445c9e8aec565d87c383c93e5f395155b82718caa5f83e134ad24ad6d256dbb4e0842765e1798e1c561e7269c652534de8ca2dc6577b6cd6c032b2dee6aad71c646eb65e8ca3e7522cb71d98c13d0cc16be2e1710afe666154b328fcdc462d5b92bd57e6d2b1cab35cda3fb4e23b63a5e945192a7b97cda1151862a928ad915566977680fc859d2d95e9cbfa907e9818ffce0cd97ed33eda149fa605a3baacd57fab17d7429fb00fb2793676ffd48752ab4a3e848e2791671c6a2ff00a945fa4e25bb1ccd71d27d74224fe7a665fb8f23f12055dcf66d2569420ff9e8958ee6335e28a5fd6a6bd04fe7a663c943c97c47e7a665fb9f25f128e45b9bce3961db56937e744adca66af6ce92feaaf544e17bb0ccdfeb525d5451496ea7347feac5755187ad01f54b717994b474abd1f05de2f859de2fa3c0399ee171d3f9f8ca7db3ad2f518b7ba2cd5fed32eca5497e1292ce7337b7175bb2d1f4203354f7b797eb6360baa84a5f891f262b27f90d68d055786f029d773e0f83d15294e2e36d27b342f7bf198a962b1d2db8bc4bfebd5f46958c8659819a5294e6e53aa96949c9ca56b6abb7b590760dcc664b0d8cc2d7bad1a75a1a6efb29c9e8cfeeca47a38f2ccb2d767697133d2f90625d6c2612abdb570f87a8fae54e2fd607de0000000000000000000061776945d4cb73082db2c1e2e2bb6948cd1f2e6b45d4c3d782db3a35a0badc1a03cbf196a44e91c5453d18ebe25b57c4e4517cabb9fb40b2a8fa7bc9e1a5cb2f1994d17d1decb5a5c8bc67ec00eb4b9cc70d3e7326cf9177fc059f37ce80af0b3e779911c24b97cc8e4b3e6bef8fb459f31fddf681c7a72e5f321a52e5f41cb67cc7f77da5927cc7f77da070e93e51adf29ce93e63ef8fb4b24f9be7407caa8f4175875c87d093e6aeff008164a5c8bc67ec038a146dfaabb91cf1eaee21297247bdfb0b28cb963dcdfac0e48c8f426e6693860b0507b6185c2c1f5aa51479e234a72f053579782ad1e37a9719e96a50518c62b64528aea4ac05c0000000000000000000000079771b4382ab5a97d156ad4fc5a8d7a8e2466376b87e0b32c7c3ff0026a54f296a9f88c3a025164422515528904a222512112011211200940948022c822500241290191dcd61f84c66121c52c450bff0aa89bf3267a10d21bdce1f4f31c3f243859beca72b79da37780000000000000000000000001a177d6c3e866d5dfd2d3c355ff6d53ff8cea68d83bf5e1ed8dc354fa4c33875f0751bff0090d7e80944a21160251288459002c884580120940112822c9004482520091648948903bbef4b42f8cab3e2861e6ba9ca70b799336d1ae379fa1ab195389f0105d6b4dbf4c4d8e00000000000000000000000006aedfc2878380ab6d93c4526ff008a3192fec66ac46e7df9e86965f4e7f458aa327d528ca1e99234c80459105900458845900448250045822520252241290048ba412240129048b2406dbdeaa868e0a72fa4af525d8a318fa533b9980dc1d0e0f2fc32e74673f1a7297a1a33e0000000000000000000000000755df430eea6538b4b6c151aabf92b424fcc99a1d1e8edd561b85c0e369f1cf0b898afe2e0dd9f7d8f38537749f4202c8b2211640116442240925044a025164422c90048ba41224016482459200916481cf82a1c254a74f9f38c175c9dbd606f7c92870786c3d3e3851a317d6a0ae7da120000000000000000000000000056ac14a328bd924d3ea68f302a5a1783db094a0ff95b5ea3d4279c37454383c6e3a9f371589b753a8e4bccc0c7964422c8012812809459108b2008ba444517400b244245d2009160592009199dc850e131d858f25684fc47a7f84c42476bdede86963a12fa38559fddd1fc406dc0000000000000000000000000000341ef89434335c6ab6a93a15174e9518ddf7a7dc6fc34befbd43473284b8aa61293bfda8d49c5aeed1ef03a522412809459108b2008b24423912008b22117480948b22116480948b24122e90048ef7bd5d0bd5c454e6d38c3c695ff0009d192365ef5b42d4711539d5210f1637fc6077700000000000000000000000000003556fd542d5701579638aa6fad38497a646d535eefd142f85c2d4e662945f54e9cfd6901a9916442250128b2211648098a2e8845901291745628ba008ba44451c89054a459209178a08948db3bded0d0c145fd254a93ee7a1f80d53189b9f731474307868feee32f1bc2f5819400000000000000000000000000003acef8d94d4c5e5f569d18e9d584a9568478e5a12bc92e56e3a5647660079730f9852a95234a1294eaca5a11a71a751d473d9a2a36bdfa0edeb7079a7d51f95a1ef1bbe387a6a4e6a10537b66a2b49f5bda7281a37f30f34faa3f2b43de2cb7099a7d51f95a1ef1bc001a47f31734faa3f2b43de256e1b33faabf2b47de3768034aadc3e67f557e568fbc4adc4667f557e568fbc6e9006995b89ccbeaafcad1f78b2dc5e65f557e568fbc6e40069e8ee3331fab3f2b47de38331dce6330d4a75eae1e6a9d35a5371d1aae31bedd18372b2e376d4b59ba001a0322c751c656a7430f3756acdf8318c276b2db26ed64971b37d6169684210e64210ee5614b0f0836e308c5cbe738c5272eb6b69ca000000000000000000000000000000000000000000000000000000000000000000000000000007ffd9, 5);

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
-- Indices de la tabla `intereses`
--
ALTER TABLE `intereses`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `id_factura_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `intereses`
--
ALTER TABLE `intereses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
