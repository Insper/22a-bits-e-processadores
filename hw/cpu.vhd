-- File: cpu.vhd
-- Generated by MyHDL 0.11
-- Date: Sun May  1 09:41:11 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity cpu is
    port (
        inMem: in unsigned(15 downto 0);
        instruction: in unsigned(17 downto 0);
        outMem: out unsigned(15 downto 0);
        addressM: out unsigned(14 downto 0);
        writeM: out std_logic;
        pcount: inout unsigned(14 downto 0);
        rst: in std_logic;
        clk: in std_logic
    );
end entity cpu;


architecture MyHDL of cpu is



signal pc_load: std_logic;
signal reg_a: unsigned(15 downto 0);
signal reg_d: unsigned(15 downto 0);
signal ula_ctr: unsigned(5 downto 0);
signal ula_ng: std_logic;
signal ula_out: unsigned(15 downto 0);
signal ula_x: unsigned(15 downto 0);
signal ula_y: unsigned(15 downto 0);
signal ula_zr: std_logic;
signal ula0_zx_out: unsigned(15 downto 0);
signal ula0_zy_out: unsigned(15 downto 0);
signal ula0_add_out: unsigned(15 downto 0);
signal ula0_mux_out: unsigned(15 downto 0);
signal ula0_no_out: unsigned(15 downto 0);
signal ula0_nx_out: unsigned(15 downto 0);
signal ula0_ny_out: unsigned(15 downto 0);
signal ula0_add160_out_q: unsigned(15 downto 0);
signal ula0_add160_fullAdder0_c: std_logic;
signal ula0_add160_fullAdder0_q: std_logic;
signal ula0_add160_fullAdder0_s1: std_logic;
signal ula0_add160_fullAdder0_carry: std_logic;
signal ula0_add160_fullAdder0_s2: std_logic;
signal ula0_add160_fullAdder0_s3: std_logic;
signal ula0_add160_fullAdder1_q: std_logic;
signal ula0_add160_fullAdder1_s1: std_logic;
signal ula0_add160_fullAdder1_carry: std_logic;
signal ula0_add160_fullAdder1_s2: std_logic;
signal ula0_add160_fullAdder1_s3: std_logic;
signal ula0_add160_fullAdder2_q: std_logic;
signal ula0_add160_fullAdder2_s1: std_logic;
signal ula0_add160_fullAdder2_carry: std_logic;
signal ula0_add160_fullAdder2_s2: std_logic;
signal ula0_add160_fullAdder2_s3: std_logic;
signal ula0_add160_fullAdder3_q: std_logic;
signal ula0_add160_fullAdder3_s1: std_logic;
signal ula0_add160_fullAdder3_carry: std_logic;
signal ula0_add160_fullAdder3_s2: std_logic;
signal ula0_add160_fullAdder3_s3: std_logic;
signal ula0_add160_fullAdder4_q: std_logic;
signal ula0_add160_fullAdder4_s1: std_logic;
signal ula0_add160_fullAdder4_carry: std_logic;
signal ula0_add160_fullAdder4_s2: std_logic;
signal ula0_add160_fullAdder4_s3: std_logic;
signal ula0_add160_fullAdder5_q: std_logic;
signal ula0_add160_fullAdder5_s1: std_logic;
signal ula0_add160_fullAdder5_carry: std_logic;
signal ula0_add160_fullAdder5_s2: std_logic;
signal ula0_add160_fullAdder5_s3: std_logic;
signal ula0_add160_fullAdder6_q: std_logic;
signal ula0_add160_fullAdder6_s1: std_logic;
signal ula0_add160_fullAdder6_carry: std_logic;
signal ula0_add160_fullAdder6_s2: std_logic;
signal ula0_add160_fullAdder6_s3: std_logic;
signal ula0_add160_fullAdder7_q: std_logic;
signal ula0_add160_fullAdder7_s1: std_logic;
signal ula0_add160_fullAdder7_carry: std_logic;
signal ula0_add160_fullAdder7_s2: std_logic;
signal ula0_add160_fullAdder7_s3: std_logic;
signal ula0_add160_fullAdder8_q: std_logic;
signal ula0_add160_fullAdder8_s1: std_logic;
signal ula0_add160_fullAdder8_carry: std_logic;
signal ula0_add160_fullAdder8_s2: std_logic;
signal ula0_add160_fullAdder8_s3: std_logic;
signal ula0_add160_fullAdder9_q: std_logic;
signal ula0_add160_fullAdder9_s1: std_logic;
signal ula0_add160_fullAdder9_carry: std_logic;
signal ula0_add160_fullAdder9_s2: std_logic;
signal ula0_add160_fullAdder9_s3: std_logic;
signal ula0_add160_fullAdder10_q: std_logic;
signal ula0_add160_fullAdder10_s1: std_logic;
signal ula0_add160_fullAdder10_carry: std_logic;
signal ula0_add160_fullAdder10_s2: std_logic;
signal ula0_add160_fullAdder10_s3: std_logic;
signal ula0_add160_fullAdder11_q: std_logic;
signal ula0_add160_fullAdder11_s1: std_logic;
signal ula0_add160_fullAdder11_carry: std_logic;
signal ula0_add160_fullAdder11_s2: std_logic;
signal ula0_add160_fullAdder11_s3: std_logic;
signal ula0_add160_fullAdder12_q: std_logic;
signal ula0_add160_fullAdder12_s1: std_logic;
signal ula0_add160_fullAdder12_carry: std_logic;
signal ula0_add160_fullAdder12_s2: std_logic;
signal ula0_add160_fullAdder12_s3: std_logic;
signal ula0_add160_fullAdder13_q: std_logic;
signal ula0_add160_fullAdder13_s1: std_logic;
signal ula0_add160_fullAdder13_carry: std_logic;
signal ula0_add160_fullAdder13_s2: std_logic;
signal ula0_add160_fullAdder13_s3: std_logic;
signal ula0_add160_fullAdder14_q: std_logic;
signal ula0_add160_fullAdder14_s1: std_logic;
signal ula0_add160_fullAdder14_carry: std_logic;
signal ula0_add160_fullAdder14_s2: std_logic;
signal ula0_add160_fullAdder14_s3: std_logic;
signal ula0_add160_fullAdder15_q: std_logic;
signal ula0_add160_fullAdder15_s1: std_logic;
signal ula0_add160_fullAdder15_carry: std_logic;
signal ula0_add160_fullAdder15_s2: std_logic;
signal ula0_add160_fullAdder15_s3: std_logic;

begin


ula0_add160_fullAdder0_c <= '0';

ula0_add160_out_q(15) <= ula0_add160_fullAdder15_q;
ula0_add160_out_q(14) <= ula0_add160_fullAdder14_q;
ula0_add160_out_q(13) <= ula0_add160_fullAdder13_q;
ula0_add160_out_q(12) <= ula0_add160_fullAdder12_q;
ula0_add160_out_q(11) <= ula0_add160_fullAdder11_q;
ula0_add160_out_q(10) <= ula0_add160_fullAdder10_q;
ula0_add160_out_q(9) <= ula0_add160_fullAdder9_q;
ula0_add160_out_q(8) <= ula0_add160_fullAdder8_q;
ula0_add160_out_q(7) <= ula0_add160_fullAdder7_q;
ula0_add160_out_q(6) <= ula0_add160_fullAdder6_q;
ula0_add160_out_q(5) <= ula0_add160_fullAdder5_q;
ula0_add160_out_q(4) <= ula0_add160_fullAdder4_q;
ula0_add160_out_q(3) <= ula0_add160_fullAdder3_q;
ula0_add160_out_q(2) <= ula0_add160_fullAdder2_q;
ula0_add160_out_q(1) <= ula0_add160_fullAdder1_q;
ula0_add160_out_q(0) <= ula0_add160_fullAdder0_q;

CPU_ULA0_ZERADOR0_COMB: process (ula_ctr, ula_x) is
begin
    if (ula_ctr(5) = '1') then
        ula0_zx_out <= to_unsigned(0, 16);
    else
        ula0_zx_out <= ula_x;
    end if;
end process CPU_ULA0_ZERADOR0_COMB;

CPU_ULA0_INVERSOR0_COMB: process (ula_ctr, ula0_zx_out) is
begin
    if (ula_ctr(4) = '1') then
        ula0_nx_out <= (not ula0_zx_out);
    else
        ula0_nx_out <= ula0_zx_out;
    end if;
end process CPU_ULA0_INVERSOR0_COMB;

CPU_ULA0_ZERADOR1_COMB: process (ula_ctr, ula_y) is
begin
    if (ula_ctr(3) = '1') then
        ula0_zy_out <= to_unsigned(0, 16);
    else
        ula0_zy_out <= ula_y;
    end if;
end process CPU_ULA0_ZERADOR1_COMB;

CPU_ULA0_INVERSOR1_COMB: process (ula_ctr, ula0_zy_out) is
begin
    if (ula_ctr(2) = '1') then
        ula0_ny_out <= (not ula0_zy_out);
    else
        ula0_ny_out <= ula0_zy_out;
    end if;
end process CPU_ULA0_INVERSOR1_COMB;


ula0_add160_fullAdder0_s2 <= (ula0_nx_out(0) and ula0_ny_out(0));
ula0_add160_fullAdder0_s1 <= (ula0_nx_out(0) xor ula0_ny_out(0));


ula0_add160_fullAdder0_s3 <= (ula0_add160_fullAdder0_c and ula0_add160_fullAdder0_s1);
ula0_add160_fullAdder0_q <= (ula0_add160_fullAdder0_c xor ula0_add160_fullAdder0_s1);


ula0_add160_fullAdder0_carry <= (ula0_add160_fullAdder0_s2 or ula0_add160_fullAdder0_s3);


ula0_add160_fullAdder1_s2 <= (ula0_nx_out(1) and ula0_ny_out(1));
ula0_add160_fullAdder1_s1 <= (ula0_nx_out(1) xor ula0_ny_out(1));


ula0_add160_fullAdder1_s3 <= (ula0_add160_fullAdder0_carry and ula0_add160_fullAdder1_s1);
ula0_add160_fullAdder1_q <= (ula0_add160_fullAdder0_carry xor ula0_add160_fullAdder1_s1);


ula0_add160_fullAdder1_carry <= (ula0_add160_fullAdder1_s2 or ula0_add160_fullAdder1_s3);


ula0_add160_fullAdder2_s2 <= (ula0_nx_out(2) and ula0_ny_out(2));
ula0_add160_fullAdder2_s1 <= (ula0_nx_out(2) xor ula0_ny_out(2));


ula0_add160_fullAdder2_s3 <= (ula0_add160_fullAdder1_carry and ula0_add160_fullAdder2_s1);
ula0_add160_fullAdder2_q <= (ula0_add160_fullAdder1_carry xor ula0_add160_fullAdder2_s1);


ula0_add160_fullAdder2_carry <= (ula0_add160_fullAdder2_s2 or ula0_add160_fullAdder2_s3);


ula0_add160_fullAdder3_s2 <= (ula0_nx_out(3) and ula0_ny_out(3));
ula0_add160_fullAdder3_s1 <= (ula0_nx_out(3) xor ula0_ny_out(3));


ula0_add160_fullAdder3_s3 <= (ula0_add160_fullAdder2_carry and ula0_add160_fullAdder3_s1);
ula0_add160_fullAdder3_q <= (ula0_add160_fullAdder2_carry xor ula0_add160_fullAdder3_s1);


ula0_add160_fullAdder3_carry <= (ula0_add160_fullAdder3_s2 or ula0_add160_fullAdder3_s3);


ula0_add160_fullAdder4_s2 <= (ula0_nx_out(4) and ula0_ny_out(4));
ula0_add160_fullAdder4_s1 <= (ula0_nx_out(4) xor ula0_ny_out(4));


ula0_add160_fullAdder4_s3 <= (ula0_add160_fullAdder3_carry and ula0_add160_fullAdder4_s1);
ula0_add160_fullAdder4_q <= (ula0_add160_fullAdder3_carry xor ula0_add160_fullAdder4_s1);


ula0_add160_fullAdder4_carry <= (ula0_add160_fullAdder4_s2 or ula0_add160_fullAdder4_s3);


ula0_add160_fullAdder5_s2 <= (ula0_nx_out(5) and ula0_ny_out(5));
ula0_add160_fullAdder5_s1 <= (ula0_nx_out(5) xor ula0_ny_out(5));


ula0_add160_fullAdder5_s3 <= (ula0_add160_fullAdder4_carry and ula0_add160_fullAdder5_s1);
ula0_add160_fullAdder5_q <= (ula0_add160_fullAdder4_carry xor ula0_add160_fullAdder5_s1);


ula0_add160_fullAdder5_carry <= (ula0_add160_fullAdder5_s2 or ula0_add160_fullAdder5_s3);


ula0_add160_fullAdder6_s2 <= (ula0_nx_out(6) and ula0_ny_out(6));
ula0_add160_fullAdder6_s1 <= (ula0_nx_out(6) xor ula0_ny_out(6));


ula0_add160_fullAdder6_s3 <= (ula0_add160_fullAdder5_carry and ula0_add160_fullAdder6_s1);
ula0_add160_fullAdder6_q <= (ula0_add160_fullAdder5_carry xor ula0_add160_fullAdder6_s1);


ula0_add160_fullAdder6_carry <= (ula0_add160_fullAdder6_s2 or ula0_add160_fullAdder6_s3);


ula0_add160_fullAdder7_s2 <= (ula0_nx_out(7) and ula0_ny_out(7));
ula0_add160_fullAdder7_s1 <= (ula0_nx_out(7) xor ula0_ny_out(7));


ula0_add160_fullAdder7_s3 <= (ula0_add160_fullAdder6_carry and ula0_add160_fullAdder7_s1);
ula0_add160_fullAdder7_q <= (ula0_add160_fullAdder6_carry xor ula0_add160_fullAdder7_s1);


ula0_add160_fullAdder7_carry <= (ula0_add160_fullAdder7_s2 or ula0_add160_fullAdder7_s3);


ula0_add160_fullAdder8_s2 <= (ula0_nx_out(8) and ula0_ny_out(8));
ula0_add160_fullAdder8_s1 <= (ula0_nx_out(8) xor ula0_ny_out(8));


ula0_add160_fullAdder8_s3 <= (ula0_add160_fullAdder7_carry and ula0_add160_fullAdder8_s1);
ula0_add160_fullAdder8_q <= (ula0_add160_fullAdder7_carry xor ula0_add160_fullAdder8_s1);


ula0_add160_fullAdder8_carry <= (ula0_add160_fullAdder8_s2 or ula0_add160_fullAdder8_s3);


ula0_add160_fullAdder9_s2 <= (ula0_nx_out(9) and ula0_ny_out(9));
ula0_add160_fullAdder9_s1 <= (ula0_nx_out(9) xor ula0_ny_out(9));


ula0_add160_fullAdder9_s3 <= (ula0_add160_fullAdder8_carry and ula0_add160_fullAdder9_s1);
ula0_add160_fullAdder9_q <= (ula0_add160_fullAdder8_carry xor ula0_add160_fullAdder9_s1);


ula0_add160_fullAdder9_carry <= (ula0_add160_fullAdder9_s2 or ula0_add160_fullAdder9_s3);


ula0_add160_fullAdder10_s2 <= (ula0_nx_out(10) and ula0_ny_out(10));
ula0_add160_fullAdder10_s1 <= (ula0_nx_out(10) xor ula0_ny_out(10));


ula0_add160_fullAdder10_s3 <= (ula0_add160_fullAdder9_carry and ula0_add160_fullAdder10_s1);
ula0_add160_fullAdder10_q <= (ula0_add160_fullAdder9_carry xor ula0_add160_fullAdder10_s1);


ula0_add160_fullAdder10_carry <= (ula0_add160_fullAdder10_s2 or ula0_add160_fullAdder10_s3);


ula0_add160_fullAdder11_s2 <= (ula0_nx_out(11) and ula0_ny_out(11));
ula0_add160_fullAdder11_s1 <= (ula0_nx_out(11) xor ula0_ny_out(11));


ula0_add160_fullAdder11_s3 <= (ula0_add160_fullAdder10_carry and ula0_add160_fullAdder11_s1);
ula0_add160_fullAdder11_q <= (ula0_add160_fullAdder10_carry xor ula0_add160_fullAdder11_s1);


ula0_add160_fullAdder11_carry <= (ula0_add160_fullAdder11_s2 or ula0_add160_fullAdder11_s3);


ula0_add160_fullAdder12_s2 <= (ula0_nx_out(12) and ula0_ny_out(12));
ula0_add160_fullAdder12_s1 <= (ula0_nx_out(12) xor ula0_ny_out(12));


ula0_add160_fullAdder12_s3 <= (ula0_add160_fullAdder11_carry and ula0_add160_fullAdder12_s1);
ula0_add160_fullAdder12_q <= (ula0_add160_fullAdder11_carry xor ula0_add160_fullAdder12_s1);


ula0_add160_fullAdder12_carry <= (ula0_add160_fullAdder12_s2 or ula0_add160_fullAdder12_s3);


ula0_add160_fullAdder13_s2 <= (ula0_nx_out(13) and ula0_ny_out(13));
ula0_add160_fullAdder13_s1 <= (ula0_nx_out(13) xor ula0_ny_out(13));


ula0_add160_fullAdder13_s3 <= (ula0_add160_fullAdder12_carry and ula0_add160_fullAdder13_s1);
ula0_add160_fullAdder13_q <= (ula0_add160_fullAdder12_carry xor ula0_add160_fullAdder13_s1);


ula0_add160_fullAdder13_carry <= (ula0_add160_fullAdder13_s2 or ula0_add160_fullAdder13_s3);


ula0_add160_fullAdder14_s2 <= (ula0_nx_out(14) and ula0_ny_out(14));
ula0_add160_fullAdder14_s1 <= (ula0_nx_out(14) xor ula0_ny_out(14));


ula0_add160_fullAdder14_s3 <= (ula0_add160_fullAdder13_carry and ula0_add160_fullAdder14_s1);
ula0_add160_fullAdder14_q <= (ula0_add160_fullAdder13_carry xor ula0_add160_fullAdder14_s1);


ula0_add160_fullAdder14_carry <= (ula0_add160_fullAdder14_s2 or ula0_add160_fullAdder14_s3);


ula0_add160_fullAdder15_s2 <= (ula0_nx_out(15) and ula0_ny_out(15));
ula0_add160_fullAdder15_s1 <= (ula0_nx_out(15) xor ula0_ny_out(15));


ula0_add160_fullAdder15_s3 <= (ula0_add160_fullAdder14_carry and ula0_add160_fullAdder15_s1);
ula0_add160_fullAdder15_q <= (ula0_add160_fullAdder14_carry xor ula0_add160_fullAdder15_s1);


ula0_add160_fullAdder15_carry <= (ula0_add160_fullAdder15_s2 or ula0_add160_fullAdder15_s3);


ula0_add_out <= ula0_add160_out_q;

CPU_ULA0_INVERSOR2_COMB: process (ula_ctr, ula0_mux_out) is
begin
    if (ula_ctr(0) = '1') then
        ula0_no_out <= (not ula0_mux_out);
    else
        ula0_no_out <= ula0_mux_out;
    end if;
end process CPU_ULA0_INVERSOR2_COMB;

CPU_ULA0_COMPARADOR0_COMB: process (ula0_no_out) is
begin
    ula_ng <= '0';
    ula_zr <= '0';
    if (to_integer(signed(ula0_no_out(16-1 downto 0))) < 0) then
        ula_ng <= '1';
        ula_zr <= '0';
    end if;
    if (ula0_no_out = 0) then
        ula_zr <= '1';
        ula_ng <= '0';
    end if;
end process CPU_ULA0_COMPARADOR0_COMB;

CPU_ULA0_COMB: process (ula0_ny_out, ula0_add_out, ula_ctr, ula0_no_out, ula0_nx_out) is
begin
    if (ula_ctr(1) = '1') then
        ula0_mux_out <= ula0_add_out;
    else
        ula0_mux_out <= (ula0_nx_out and ula0_ny_out);
    end if;
    ula_out <= ula0_no_out(16-1 downto 0);
end process CPU_ULA0_COMB;

CPU_PC0_LOGIC: process (clk, rst) is
begin
    if (rst = '0') then
        pcount <= to_unsigned(0, 15);
    elsif rising_edge(clk) then
        if (pc_load = '1') then
            pcount <= resize(reg_a, 15);
        elsif (1 = 1) then
            pcount <= (pcount + 1);
        else
            pcount <= pcount;
        end if;
    end if;
end process CPU_PC0_LOGIC;


writeM <= instruction(5);
addressM <= resize(reg_a, 15);
outMem <= ula_out;

CPU_CONTROLUNIT: process (ula_ng, instruction, reg_a, inMem, ula_zr, reg_d) is
    variable jmp: std_logic;
begin
    ula_ctr <= instruction(13-1 downto 7);
    if (instruction(13) = '1') then
        ula_y <= inMem;
    else
        ula_y <= reg_a;
    end if;
    ula_x <= reg_d;
    jmp := '0';
    if ((instruction(17) = '1') and (instruction(3-1 downto 0) > 0)) then
        if (instruction(0) = '1') then
            if ((ula_ng = '0') and (ula_zr = '0')) then
                jmp := '1';
            end if;
        end if;
        if (instruction(1) = '1') then
            if (ula_zr = '1') then
                jmp := '1';
            end if;
        end if;
        if (instruction(2) = '1') then
            if (ula_ng = '1') then
                jmp := '1';
            end if;
        end if;
        if (instruction(3-1 downto 0) = 7) then
            jmp := '1';
        end if;
    end if;
    if bool(jmp) then
        pc_load <= '1';
    else
        pc_load <= '0';
    end if;
end process CPU_CONTROLUNIT;

CPU_REGISTERS: process (clk) is
begin
    if rising_edge(clk) then
        if (instruction(17) = '0') then
            reg_a <= instruction(16-1 downto 0);
        else
            if (instruction(3) = '1') then
                reg_a <= ula_out;
            else
                reg_a <= reg_a;
            end if;
            if (instruction(4) = '1') then
                reg_d <= ula_out;
            else
                reg_d <= reg_d;
            end if;
        end if;
    end if;
end process CPU_REGISTERS;

end architecture MyHDL;