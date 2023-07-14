-------------------------------------------------------------------------------
-- Title      : DDBEN
-- Project    : 
-------------------------------------------------------------------------------
-- File       : aes_tb.vhd
-- Author     : Francesco Regazzoni  <regazzoni@alari.ch>
-- Company    : Advanced Learning and Research Insitute, Lugano 
-- Created    : 2013-11-3
-- Last update: 2013-11-3
-- Platform   : ModelSim (simulation), Synopsys (synthesis)
-- Standard   : VHDL'87
-------------------------------------------------------------------------------
-- Description: Test bench for the AES core of Frank 
-------------------------------------------------------------------------------
-- Copyright (c) 2013 Francesco Regazzoni
-------------------------------------------------------------------------------
-- Revisions  :
-- Date        Version  Author  Description
-- 2013-11-3  1.0      rf      Created
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;
--use work.aes_pack.all;

library work;
use work.all;

entity GF64_mult_tb is
end GF64_mult_tb;


architecture tb of GF64_mult_tb is   

 signal   I1xD  :    std_logic_vector(63 downto 0);
 signal   I2xD  :    std_logic_vector(63 downto 0);
 signal   OpxD  :    std_logic_vector(63 downto 0);
 

  signal ClkxC : std_logic;                    -- driving clock
 
   




  --component GF64_mult
  --port(
  --  I1xDI : in  std_logic_vector(63 downto 0);
  --  I2xDI : in  std_logic_vector(63 downto 0);
  --  OpxDO : out std_logic_vector(63 downto 0);
  --  ClkxCI : in std_logic 
  --);
  --end component;
       


   
begin

  -- Instantiate the module under test (MUT)
	mut: entity GF64_mult
    port map (
       I1xDI  => I1xD,
       I2xDI  => I2xD,
       OpxDO  => OpxD, 
       ClkxCI => ClkxC
   );

  -- Generate the clock
--  ClkxC <= not (ClkxC) after clkphasehigh;


  Tb_clkgen : process
  begin
     ClkxC <= '1';
     wait for 50 ns;
     ClkxC <= '0';
     wait for 50 ns;
  end process Tb_clkgen;

  -- obtain stimulus and apply it to MUT
  ----------------------------------------------------------------------------
  B1 : block
   begin


  -- timing of clock and simulation events
 


  Tb_stimappli : process
    variable INLine   : line;
    variable temp_1   : STD_LOGIC_VECTOR(63 downto 0);
    variable temp_2   : STD_LOGIC_VECTOR(63 downto 0); 
    variable temp_3   : STD_LOGIC_VECTOR(63 downto 0); 
    variable temp_ed  : STD_LOGIC_VECTOR(3 downto 0);  
    constant clkphasehigh: time:= 50 ns;
    constant clkphaselow: time:= 50 ns;
 
    constant resetactivetime:         time:= 25 ns;

  -- declaration of stimuli, expected responses, and simulation report files
  file stimulifile, simreptfile : text;
  constant stimulifilename : string := "HDL/TBENCH/newstimuli.txt";
  constant simreptfilename : string := "OUT/aessim.rpt";

  file i1file,i2file,ofile,ptfile,edfile : TEXT;



  begin
    -- Opening Input File
    file_open(i1file, "../in1-64.txt", read_mode);
    file_open(i2file, "../in2-64.txt", read_mode);
    file_open(ofile, "../out-64.txt",  read_mode);
 

    -- default values

  
 

    -- process until we run out of stimuli
    --appli_loop : while not (endfile(i1file)) loop
    appli_loop : for i in 0 to 0 loop
     
    
      readline(i1file,INLine);
      hread(INLine,temp_1);
      I1xD <= temp_1;
      readline(i2file,INLine);
      hread(INLine,temp_2);
      I2xD <= temp_2;
      readline(ofile,INLine);
      hread(INLine,temp_3);
      

     
      wait for 1*clkphasehigh  ;
      assert OpxD = temp_3 report "wrong result" severity failure;
      wait for 1*clkphasehigh  ;
    
  

    end loop appli_loop;
    wait until ClkxC'event and ClkxC = '1';
    file_close(i1file);
    file_close(i2file);
    file_close(ofile);
    assert false report "test passed" severity failure;

  end process Tb_stimappli;
end block;
end tb;
