// Copyright (C) by Josh Blum. See LICENSE.txt for licensing information.

#ifndef INCLUDED_GREXTRAS_MULTIPLY_HPP
#define INCLUDED_GREXTRAS_MULTIPLY_HPP

#include <grextras/config.hpp>
#include <gras/block.hpp>

namespace grextras
{

/*!
 * Multiply block, one output, multiple outputs.
 * This block uses C++ templates to create multiple implementations.
 */
struct GREXTRAS_API Multiply : virtual gras::Block
{
    typedef boost::shared_ptr<Multiply> sptr;

    static sptr make_fc32_fc32(const size_t vlen = 1);
    static sptr make_sc32_sc32(const size_t vlen = 1);
    static sptr make_sc16_sc16(const size_t vlen = 1);
    static sptr make_sc8_sc8(const size_t vlen = 1);
    static sptr make_f32_f32(const size_t vlen = 1);
    static sptr make_s32_s32(const size_t vlen = 1);
    static sptr make_s16_s16(const size_t vlen = 1);
    static sptr make_s8_s8(const size_t vlen = 1);
};

}

#endif /*INCLUDED_GREXTRAS_MULTIPLY_HPP*/
