// Copyright (c) 2019 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_UTILITIES_H
#define HYPERFLUX_UTILITIES_H

#include <algorithm>

namespace hyperflux {
namespace utilities {

template <class InputIt, class UnaryPredicate>
constexpr InputIt find_if_precedent(InputIt first, InputIt last, UnaryPredicate p)
{
    for (; first != last; ++first) {
        if (p(*(first - 1), *first)) {
            return first;
        }
    }
    return last;
}

template <class ForwardIt, class UnaryPredicate>
inline ForwardIt remove_if_precedent(ForwardIt first, ForwardIt last, UnaryPredicate p)
{
    ++first;
    first = find_if_precedent(first, last, p);
    if (first != last)
        for (ForwardIt i = first; ++i != last;)
            if (!p(*(i - 1), *i))
                *first++ = std::move(*i);
    return first;
}

}  // namespace utilities
}  // namespace hyperflux

#endif