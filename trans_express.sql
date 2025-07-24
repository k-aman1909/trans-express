
CREATE TABLE `automatic1` (
  `dipo_id` int(11) DEFAULT NULL,
  `dist_id` int(11) DEFAULT NULL,
  `trans_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `dipo_details` (
  `dipo_id` varchar(100) DEFAULT NULL,
  `pri_name` varchar(500) DEFAULT NULL,
  `ope_name` varchar(1000) DEFAULT NULL,
  `man_name` varchar(1000) DEFAULT NULL,
  `man_cont` varchar(50) DEFAULT NULL,
  `dipo_cont` varchar(50) DEFAULT NULL,
  `dipo_tel` varchar(50) DEFAULT NULL,
  `state1` varchar(1000) DEFAULT NULL,
  `distr` varchar(1000) DEFAULT NULL,
  `addr` varchar(2000) DEFAULT NULL,
  `gst` varchar(100) DEFAULT NULL,
  `auto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Table structure for table `distributor_details`
--

CREATE TABLE `distributor_details` (
  `dist_id` varchar(100) DEFAULT NULL,
  `dist_name` varchar(1000) DEFAULT NULL,
  `cont_no` varchar(50) DEFAULT NULL,
  `dipo_name` varchar(1000) DEFAULT NULL,
  `addrs` varchar(2000) DEFAULT NULL,
  `state1` varchar(1000) DEFAULT NULL,
  `city` varchar(1000) DEFAULT NULL,
  `landline_no` varchar(50) DEFAULT NULL,
  `dipo_id` varchar(100) DEFAULT NULL,
  `gst_no` varchar(100) DEFAULT NULL,
  `le_ex` varchar(1000) DEFAULT NULL,
  `pin` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `plorder`
--

CREATE TABLE `plorder` (
  `lrno` varchar(100) DEFAULT NULL,
  `lrdate` date DEFAULT NULL,
  `dname` varchar(500) DEFAULT NULL,
  `dtown` varchar(500) DEFAULT NULL,
  `tname` varchar(500) DEFAULT NULL,
  `vno` varchar(100) DEFAULT NULL,
  `vtype` varchar(500) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `ino` varchar(100) DEFAULT NULL,
  `ivalue` varchar(500) DEFAULT NULL,
  `idate` varchar(100) DEFAULT NULL,
  `quantity` varchar(100) DEFAULT NULL,
  `weight` varchar(100) DEFAULT NULL,
  `freight` varchar(100) DEFAULT NULL,
  `le` varchar(100) DEFAULT NULL,
  `ta` varchar(100) DEFAULT NULL,
  `aa` varchar(500) DEFAULT NULL,
  `da` varchar(100) DEFAULT NULL,
  `dipo_id` varchar(100) DEFAULT NULL,
  `m_ch` varchar(500) DEFAULT NULL,
  `pd` varchar(1000) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `plvehicle`
--

CREATE TABLE `plvehicle` (
  `vtype` varchar(1000) DEFAULT NULL,
  `vprise` varchar(1000) DEFAULT NULL,
  `cname` varchar(1000) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `dipo_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `pl_sign`
--

CREATE TABLE `pl_sign` (
  `s_n` int(11) NOT NULL,
  `U_NAME` varchar(1000) DEFAULT NULL,
  `U_ID` varchar(1000) DEFAULT NULL,
  `P_WORD` varchar(1000) DEFAULT NULL,
  `S_QUESTIONS` varchar(1000) DEFAULT NULL,
  `S_ANSWER` varchar(1000) DEFAULT NULL,
  `R_O_L_E` varchar(1000) DEFAULT NULL,
  `SATU` varchar(1000) DEFAULT NULL,
  `dipo_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-
--
-- Table structure for table `state1`
--

CREATE TABLE `state1` (
  `stat` varchar(500) DEFAULT NULL,
  `distr` varchar(6500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `state1`
--

INSERT INTO `state1` (`stat`, `distr`) VALUES
('Uttar Pradesh', 'Agra,Aligarh,Allahabad,Ambedkar Nagar,Amethi,Amroha,Auraiya,Azamgarh,Baghpat,Bahraich,Ballia,Balrampur,Banda,Barabanki,Bareilly,Basti,Bhadohi,Bijnor,Budaun,Bulandshahr,Chandauli,Chitrakoot,Deoria,Etah,Etawah,Faizabad,Farrukhabad,Fatehpur,Firozabad,Gautam Buddha Nagar (Noida),Ghaziabad,,Ghazipur,Gonda,Gorakhpur,Hamirpur,Hapur (Panchsheel Nagar),Hardoi,Hathras,Jalaun,Jaunpur,Jhansi,Kannauj,Kanpur Dehat,Kanpur Nagar,Kasganj,Kaushambi,Kushinagar,Lakhimpur Kheri,Lalitpur,Lucknow,Maharajganj,Mahoba,Mainpuri,Mathura,Mau,Meerut,Mirzapur,Moradabad,Muzaffarnagar,Pilibhit,Pratapgarh,Raebareli,Rampur,Saharanpur,Sambhal,Sant Kabir Nagar,Sant Ravidas Nagar (Bhadohi),Shahjahanpur,Shamli,Shravasti,Siddharthnagar,Sitapur,Sonbhadra,Sultanpur,Unnao'),
('Andhra Pradesh', 'Anantapur,Chittoor,East Godavari,Guntur,Krishna,Kurnool,Nellore,Prakasam,Srikakulam,Visakhapatnam,Vizianagaram,West Godavari,Kadapa (YSR)'),
('Arunachal Pradesh', 'Tawang,West Kameng,East Kameng,Papumpare,Kurung Kumey,Kra Daadi,Lower Subansiri,Upper Subansiri,West Siang,East Siang,Siang,Upper Siang,Dibang Valley,Lower Dibang Valley,Lohit,Namsai,Anjaw,Changlang,Tirap,Longding'),
('Assam', 'Baksa,Barpeta,Biswanath,Bongaigaon,Cachar,Charaideo,Chirang,Darrang,Dhemaji,Dhubri,Dibrugarh,Dima Hasao,Goalpara,Golaghat,Hailakandi,Hojai,Jorhat,Kamrup,Kamrup Metropolitan,Karbi Anglong,Karimganj,Kokrajhar,Lakhimpur,Majuli,Morigaon,Nagaon,Nalbari,Dima Hasao,Sivasagar,Sonitpur,South Salamara-Mankachar,Tinsukia,Udalguri,West Karbi Anglong'),
('Chattisgarh', 'Balod,Baloda Bazar,Balrampur,Bastar,Bemetara,Bijapur,Bilaspur,Dantewada,Dhamtari,Durg,Gariaband,Janjgir-Champa,Jashpur,Kanker,Kabirdham,Korba,Kondagaon,Mahasamund,Mungeli,Narayanpur,Raigarh,Raipur,Rajnandgaon,Sukma,Surajpur,Surguja'),
('Delhi', 'Central Delhi,East Delhi,New Delhi,North Delhi,North East Delhi,North West Delhi,Shahdara,South Delhi,South East Delhi,South West Delhi,West Delhi'),
('Goa', 'North Goa,South Goa'),
('Andaman & Nicobar', 'Nicobar district,North and Middle Andaman district,South Andaman district'),
('Gujarat', 'Ahmedabad,Amreli,Anand,Aravalli,Banaskantha (Palanpur),Bharuch,Bhavnagar,Botad,Chhota Udepur,Dahod,Dangs (Ahwa),Devbhoomi Dwarka,Gandhinagar,Gir Somnath,Jamnagar,Junagadh,Kheda (Nadiad),Kutch (Bhuj),Mahisagar (Lunavada),Mehsana,Morbi,Narmada (Rajpipla),Navsari,Panchmahal (Godhra),Patan,Porbandar,Rajkot,Sabarkantha (Himmatnagar),Surat,Surendranagar,Tapi (Vyara),Vadodara,Valsad'),
('Haryana', 'Ambala,Bhiwani,Charkhi Dadri,Faridabad,Fatehabad,Gurugram (Gurgaon),Hisar,Jhajjar,Jind,Kaithal,Karnal,Kurukshetra,Mahendragarh,Nuh,Palwal,Panchkula,Panipat,Rewari,Rohtak,Sirsa,Sonipat,Yamunanagar'),
('Himachal Pradesh', 'Bilaspur,Chamba,Hamirpur,Kangra,Kinnaur,Kullu,Lahaul and Spiti.Mandi,Shimla,Sirmaur,Solan,Una'),
('Jammu & Kashmir', 'Anantnag,Bandipora,Baramulla,Budgam,Doda,Ganderbal,Jammu,Kathua,Kishtwar,Kulgam,Kupwara,Leh,Poonch,Pulwama,Rajouri,Ramban,Reasi,Samba,Shopian,Srinagar'),
('Jharkhand', 'Bokaro,Chatra,Deoghar,Dhanbad,Dumka,East Singhbhum (Jamshedpur),Garhwa,Giridih,Godda,Gumla,Hazaribagh,Jamtara,Khunti,Koderma,Latehar,Lohardaga,Pakur,Palamu,Ramgarh,Ranchi,Sahibganj,Seraikela-Kharsawan,Simdega,West Singhbhum (Chaibasa)'),
('Karnataka', 'Bagalkot,Ballari (Bellary),Belagavi (Belgaum),Bengaluru (Bangalore) Rural,Bengaluru (Bangalore) Urban,Bidar,Chamarajanagar,Chikballapur,Chikkamagaluru (Chikmagalur),Chitradurga,Dakshina Kannada,Davangere,Dharwad,Gadag,Hassan,Haveri,Kalaburagi (Gulbarga),Kodagu,Kolar,Koppal,Mandya,Mysuru (Mysore),Raichur,Ramanagara,Shivamogga (Shimoga),Tumakuru (Tumkur),Udupi,Uttara Kannada (Karwar),Vijayapura (Bijapur),Yadgir'),
('Kerala', 'Alappuzha,Ernakulam,Idukki,Kannur,Kasaragod,Kollam,Kottayam,Kozhikode,Malappuram,Palakkad,Pathanamthitta,Thiruvananthapuram,Thrissur,Wayanad'),
('Lakshadweep', 'Lakshadweep'),
('Madhya Pradesh', 'Agar Malwa,Alirajpur,Anuppur,Ashoknagar,Balaghat,Barwani,Betul,Bhind,Bhopal,Burhanpur,Chhatarpur,Chhindwara,Damoh,Datia,Dewas,Dhar,Guna,Gwalior,Harda,Hoshangabad,Indore,Jabalpur,Katni,Khandwa,Khargone,Mandla,Mandsaur,Morena,Narsinghpur,Narayanpur,Neemuch,Panna,Raisen,Rajgarh,Ratlam,Rewa,Sagar,Satna,Sehore,Seoni,Shahdol,Shajapur,Sheopur,Shivpuri,Sidhi,Singrauli,Tikamgarh,Ujjain,Umaria,Vidisha'),
('Maharashtra', 'Ahmednagar,Akola,Amravati,Aurangabad,Beed,Bhandara,Buldhana,Chandrapur,Dhule,Gadchiroli,Gondia,Hingoli,Jalgaon,Jalna,Kolhapur,Latur,Mumbai,Nagpur,Nanded,Nandurbar,Nashik,Osmanabad,Palghar,Parbhani,Pune,Raigad,Ratnagiri,Sangli,Satara,Sindhudurg,Solapur,Thane,Wardha,Washim,Yavatmal'),
('Manipur', 'Bishnupur,Chandel,Churachandpur,Imphal East,Imphal West,Jiribam,Kakching,Kamjong,Kangpokpi,Noney,Pherzawl,Senapati,Tamenglong,Tengnoupal,Thoubal,Ukhrul'),
('Meghalaya', 'East Garo Hills,West Garo Hills,South Garo Hills,North Garo Hills,South West Garo Hills,East Khasi Hills,West Khasi Hills,South West Khasi Hills,Ri Bhoi,East Jaintia Hills,West Jaintia Hills'),
('Mizoram', 'Aizawl,Champhai,Kolasib,Lawngtlai,Lunglei,Mamit,Saiha,Serchhip'),
('Nagaland', 'Dimapur,Kiphire,Kohima,Longleng,Mokokchung,Mon,Peren,Phek,Tuensang,Wokha,Zunheboto'),
('Odisha', 'Angul,Balangir,Balasore,Bargarh,Bhadrak,Boudh,Cuttack,Deogarh,Dhenkanal,Gajapati,Ganjam,Jagatsinghpur,Jajpur,Jharsuguda,Kalahandi,Kandhamal,Kendrapara,Kendujhar (Keonjhar),Khordha,Koraput,Malkangiri,Mayurbhanj,Nabarangpur,Nayagarh,Nuapada,Puri,Rayagada,Sambalpur,Sonepur,Sundargarh'),
('Punjab', 'Amritsar,Barnala,Bathinda,Faridkot,Fatehgarh Sahib,Fazilka,Ferozepur,Gurdaspur,Hoshiarpur,Jalandhar,Kapurthala,Ludhiana,Mansa,Moga,Muktsar,Nawanshahr (Shahid Bhagat Singh Nagar),Pathankot,Patiala,Rupnagar,Sahibzada Ajit Singh Nagar (Mohali),Sangrur,Tarn Taran'),
('Rajasthan', 'Ajmer,Alwar,Banswara,Baran,Barmer,Bharatpur,Bhilwara,Bikaner,Bundi,Chittorgarh,Churu,Dausa,Dholpur,Dungarpur,Hanumangarh,Jaipur,,Jaisalmer,Jalore,Jhalawar,Jhunjhunu,,,Jodhpur,Karauli,Kota,Nagaur,Pali,Pratapgarh,Rajsamand,Sawai Madhopur,Sikar,Sirohi,Sri Ganganagar,Tonk,Udaipur'),
('Sikkim', 'East Sikkim,North Sikkim,South Sikkim,West Sikkim'),
('Tamil Nadu', 'Ariyalur,Chennai,Coimbatore,Cuddalore,Dharmapuri,Dindigul,Erode,Kanchipuram,Kanyakumari,Karur,Krishnagiri,Madurai,Nagapattinam,Namakkal,Nilgiris,Perambalur,Pudukkottai,Ramanathapuram,Salem,Sivaganga,Thanjavur,Theni,Thoothukudi (Tuticorin),Tiruchirappalli (Trichy),Tirunelveli,Tirupathur,Tiruppur,Tiruvallur,Tiruvannamalai,Tiruvarur,Vellore,Viluppuram,Virudhunagar'),
('Telangana', 'Adilabad,Bhadradri Kothagudem,Hyderabad,Jagitial,Jangaon,Jayashankar Bhupalpally,Jogulamba Gadwal,Kamareddy,Karimnagar,Khammam,Komaram Bheem Asifabad,Mahabubabad,Mahabubnagar,Mancherial,Medak,Medchal-Malkajgiri,Mulugu,Nagarkurnool,Nalgonda,Narayanpet,Nirmal,Nizamabad,Peddapalli,Rajanna Sircilla,Ranga Reddy,Sangareddy,Siddipet,Suryapet,Vikarabad,Wanaparthy,Warangal Rural,Warangal Urban,Yadadri Bhuvanagiri'),
('Tripura', 'Dhalai,Gomati,Khowai,North Tripura,Sepahijala,South Tripura,Unakoti,West Tripura'),
('Uttarakhand', 'Almora,Bageshwar,Chamoli,Champawat,Dehradun,Haridwar,Nainital,Pauri Garhwal,Pithoragarh,Rudraprayag,Tehri Garhwal,Udham Singh Nagar,Uttarkashi'),
('West Bengal', 'Alipurduar,Bankura,Birbhum,Cooch Behar,Dakshin Dinajpur (South Dinajpur),Darjeeling,Hooghly,Howrah,Jalpaiguri,Jhargram,Kalimpong,Kolkata (formerly Calcutta),Malda,Murshidabad,Nadia,North 24 Parganas,Paschim Bardhaman (West Bardhaman),Paschim Medinipur (West Medinipur),Purba Bardhaman (East Bardhaman),Purba Medinipur (East Medinipur),Purulia,South 24 Parganas,Uttar Dinajpur (North Dinajpur)'),
('Chandigarh', 'Lakshadweep'),
('Dadra & Nagar Haveli and Daman & Diu', 'Dadra and Nagar Haveli and Daman,Diu'),
('Pondicherry', 'Karaikal,Mahe,Pondicherry,Yanam'),
('Bihar', 'Araria,Arwal,Aurangabad,Banka,Begusarai,Bhagalpur,Bhojpur,Buxar,Darbhanga,East Champaran(Motihari),Gaya,Gopalganj,Jamui,Jehanabad,Kaimur(Bhabua),Katihar,Khagaria,Kishanganj,Lakhisarai,Madhepura,Madhubani,Munger(Monghyr),Muzaffarpur,Nalanda,Nawada,Patna,Purnia(Purnea),Rohtas,Saharsa,Samastipur,Saran,Sheikhpura,Sheohar,Sitamarhi,Siwan,Supaul,Vaishali,West Champaran(Bettiah),Patna Transport Nagar');

-- --------------------------------------------------------

--
-- Table structure for table `transporter_details`
--

CREATE TABLE `transporter_details` (
  `trans_id` varchar(1000) DEFAULT NULL,
  `trans_name` varchar(1000) DEFAULT NULL,
  `cont_no` varchar(50) DEFAULT NULL,
  `land_no` varchar(50) DEFAULT NULL,
  `prop_name` varchar(1000) DEFAULT NULL,
  `addrs` varchar(2000) DEFAULT NULL,
  `state1` varchar(1000) DEFAULT NULL,
  `distr` varchar(1000) DEFAULT NULL,
  `bnk_name` varchar(1000) DEFAULT NULL,
  `acchold_name` varchar(1000) DEFAULT NULL,
  `acc_no` varchar(100) DEFAULT NULL,
  `ifsc` varchar(100) DEFAULT NULL,
  `veh_ty` varchar(100) DEFAULT NULL,
  `dipo_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for table `pl_sign`
--
ALTER TABLE `pl_sign`
  ADD PRIMARY KEY (`s_n`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pl_sign`
--
ALTER TABLE `pl_sign`
  MODIFY `s_n` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1126;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
