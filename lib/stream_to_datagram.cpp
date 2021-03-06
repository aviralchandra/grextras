// Copyright (C) by Josh Blum. See LICENSE.txt for licensing information.

#include <grextras/stream_to_datagram.hpp>
#include <PMC/Containers.hpp>
#include <boost/make_shared.hpp>
#include <boost/foreach.hpp>

using namespace grextras;

struct Stream2DatagramImpl : Stream2Datagram
{
    Stream2DatagramImpl(const size_t itemsize, const size_t mtu):
        gras::Block("GrExtras Stream2Datagram"),
        _mtu(itemsize*(mtu/itemsize)) //ensure mtu is a multiple
    {
        //setup the input for streaming
        this->input_config(0).item_size = itemsize;
    }

    void work(const InputItems &, const OutputItems &)
    {
        //grab the input buffer on port 0
        gras::SBuffer b = this->get_input_buffer(0);

        //clip the buffer length to the mtu
        if (_mtu) b.length = std::min(b.length, _mtu);
        const size_t items = b.length/this->input_config(0).item_size;

        //create a message for this buffer
        gras::PacketMsg msg(b);

        //save stream tags into the info
        PMCList tag_list;
        BOOST_FOREACH(const gras::Tag &tag, this->get_input_tags(0))
        {
            if (tag.offset >= this->get_consumed(0) + items) continue;
            gras::Tag new_tag = tag;
            new_tag.offset -= this->get_consumed(0);
            tag_list.push_back(PMC_M(new_tag));
        }
        if (not tag_list.empty()) msg.info = PMC_M(tag_list);

        //post the output message downstream
        this->post_output_msg(0, msg);

        //consume the number of items in b
        this->consume(0, items);
    }

    void propagate_tags(const size_t, const gras::TagIter &)
    {
        //dont propagate
    }

    const size_t _mtu;
};

Stream2Datagram::sptr Stream2Datagram::make(const size_t itemsize, const size_t mtu)
{
    return boost::make_shared<Stream2DatagramImpl>(itemsize, mtu);
}
