#
# Copyright 2004-2012 Free Software Foundation, Inc.
#
# This file is part of GrExtras
#
# GrExtras is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GrExtras is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GrExtras; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import unittest
import gras
import grextras
import numpy

class test_add_and_friends(unittest.TestCase):

    def setUp(self):
        self.tb = gras.TopBlock()

    def tearDown(self):
        self.tb = None

    def help_ii(self, src_data, exp_data, op):
        for s in zip(range(len(src_data)), src_data):
            src = grextras.VectorSource(numpy.int32, s[1])
            self.tb.connect(src,(op, s[0]))
        dst = grextras.VectorSink(numpy.int32)
        self.tb.connect(op, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(exp_data, result_data)

    def help_ff(self, src_data, exp_data, op):
        for s in zip(range(len(src_data)), src_data):
            src = grextras.VectorSource(numpy.float32, s[1])
            self.tb.connect(src,(op, s[0]))
        dst = grextras.VectorSink(numpy.float32)
        self.tb.connect(op, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(exp_data, result_data)

    def help_cc(self, src_data, exp_data, op):
        for s in zip(range(len(src_data)), src_data):
            src = grextras.VectorSource(numpy.complex64, s[1])
            self.tb.connect(src,(op, s[0]))
        dst = grextras.VectorSink(numpy.complex64)
        self.tb.connect(op, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(exp_data, result_data)

    def test_add_const_ii(self):
        src_data =(1, 2, 3, 4, 5)
        expected_result =(6, 7, 8, 9, 10)
        op = grextras.AddConst.s32_s32(5)
        self.help_ii((src_data,), expected_result, op)

    def test_add_const_cc(self):
        src_data =(1, 2, 3, 4, 5)
        expected_result =(1+5j, 2+5j, 3+5j, 4+5j, 5+5j)
        op = grextras.AddConst.fc32_fc32(5j)
        self.help_cc((src_data,), expected_result, op)

    def test_add_const_cc_1(self):
        src_data =(1, 2, 3, 4, 5)
        expected_result =(3+5j, 4+5j, 5+5j, 6+5j, 7+5j)
        op = grextras.AddConst.fc32_fc32(2+5j)
        self.help_cc((src_data,), expected_result, op)

    def test_add_const_ff(self):
        src_data =(1, 2, 3, 4, 5)
        expected_result =(6, 7, 8, 9, 10)
        op = grextras.AddConst.f32_f32(5)
        self.help_ff((src_data,), expected_result, op)

    def test_mult_const_ii(self):
        src_data =(-1, 0, 1, 2, 3)
        expected_result =(-5, 0, 5, 10, 15)
        op = grextras.MultiplyConst.s32_s32(5)
        self.help_ii((src_data,), expected_result, op)

    def test_mult_const_cc(self):
        src_data =(-1-1j, 0+0j, 1+1j, 2+2j, 3+3j)
        expected_result =(1-5j,  0+0j, -1+5j, -2+10j,(-3+15j))
        op = grextras.MultiplyConst.fc32_fc32(2+3j)
        self.help_cc((src_data,), expected_result, op)

    def test_mult_const_ff(self):
        src_data =(-1, 0, 1, 2)
        expected_result =(-5., 0., 5., 10.)
        op = grextras.MultiplyConst.f32_f32(5)
        self.help_ff((src_data,), expected_result, op)

    def test_add_ii(self):
        src1_data =(1,  2, 3, 4, 5)
        src2_data =(8, -3, 4, 8, 2)
        expected_result =(9, -1, 7, 12, 7)
        op = grextras.Add.s32_s32()
        self.help_ii((src1_data, src2_data),
                      expected_result, op)

    def test_add_ff(self):
        src1_data =(1,  2, 3, 4)
        src2_data =(8., -3., 4., 8.)
        expected_result =(9., -1., 7., 12.)
        op = grextras.Add.f32_f32()
        self.help_ff((src1_data, src2_data),
                      expected_result, op)

    def test_add_cc(self):
        src1_data =(1+1j, 2+2j, 3+3j, 4+4j)
        src2_data =(8+8j, -3-3j, 4+4j, 8+8j)
        expected_result =(9+9j, -1-1j, 7+7j, 12+12j)
        op = grextras.Add.fc32_fc32()
        self.help_cc((src1_data, src2_data),
                      expected_result, op)

    def test_mult_ii(self):
        src1_data =(1,  2, 3, 4, 5)
        src2_data =(8, -3, 4, 8, 2)
        expected_result =(8, -6, 12, 32, 10)
        op = grextras.Multiply.s32_s32()
        self.help_ii((src1_data, src2_data),
                      expected_result, op)

    def test_mult_cc(self):
        src1_data =(1,  2, 3, 4)
        src2_data =(8, -3, 4, 8)
        expected_result =(8, -6, 12, 32)
        op = grextras.Multiply.fc32_fc32()
        self.help_cc((src1_data, src2_data),
                      expected_result, op)

    def test_mult_ff(self):
        src1_data =(1,  2, 3, 4)
        src2_data =(8, -3, 4, 8)
        expected_result =(8, -6, 12, 32)
        op = grextras.Multiply.f32_f32()
        self.help_ff((src1_data, src2_data),
                      expected_result, op)

    def test_sub_ii_1(self):
        src1_data =(1,  2, 3, 4, 5)
        expected_result =(-1, -2, -3, -4, -5)
        op = grextras.Subtract.s32_s32()
        self.help_ii((src1_data,),
                      expected_result, op)

    def test_sub_ii_2(self):
        src1_data =(1,  2, 3, 4, 5)
        src2_data =(8, -3, 4, 8, 2)
        expected_result =(-7, 5, -1, -4, 3)
        op = grextras.Subtract.s32_s32()
        self.help_ii((src1_data, src2_data),
                      expected_result, op)

    def test_div_ff_1(self):
        src1_data       =(1,  2,  4,    -8)
        expected_result =(1, 0.5, 0.25, -.125)
        op = grextras.Divide.f32_f32()
        self.help_ff((src1_data,),
                      expected_result, op)

    def test_div_ff_2(self):
        src1_data       =( 5,  9, -15, 1024)
        src2_data       =(10,  3,  -5,   64)
        expected_result =(0.5, 3,   3,   16)
        op = grextras.Divide.f32_f32()
        self.help_ff((src1_data, src2_data),
                      expected_result, op)

    def test_make_math_const_vs(self):
        op = grextras.AddConstV.fc32_fc32([1, 2, 4])
        op = grextras.AddConstV.f32_f32([1, 2, 4])
        op = grextras.AddConstV.s32_s32([1, 2, 4])
        op = grextras.MultiplyConstV.fc32_fc32([1, 2, 4])
        op = grextras.MultiplyConstV.f32_f32([1, 2, 4])
        op = grextras.MultiplyConstV.s32_s32([1, 2, 4])

    def test_set_math_const_vs(self):
        op = grextras.AddConstV.fc32_fc32([1, 2, 4])
        op.set_const([0, 5, 6])
        op = grextras.MultiplyConstV.fc32_fc32([1, 2, 4])
        op.set_const([0, 5, 6])

if __name__ == '__main__':
    unittest.main()
