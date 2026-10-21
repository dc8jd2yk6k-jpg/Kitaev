# Narration script

Voice-over for *Unpaired Majoranas* (generated from `src/narration.py`).

## Cold open

Take a single electron. Now imagine you could cut it in half.

Not physically, of course. But mathematically, every electron can be written as two halves: two strange objects called Majorana fermions.

Normally the two halves are glued together, sitting on the same atom. But in the year 2000, Alexei Kitaev wrote down a simple model of a wire where the halves come unstuck,

and end up at opposite ends of the wire, as far apart as you like.

One electron's worth of quantum information, stored nowhere in particular. And that makes it remarkably hard to destroy.

This is the story of one short, beautiful paper.

## 1 · Why quantum memory is fragile

To see why this matters, start with the problem Kitaev wanted to solve: quantum memory.

A qubit can be zero, one, or any superposition of the two. And it is fragile in two distinct ways.

A classical error, σˣ, flips zero into one.

A phase error, σᶻ, leaves the bits alone, but flips the sign of the one part relative to the zero part, quietly scrambling the superposition.

Error-correcting codes can fix both, but only if every gate fails less than about once in ten thousand tries. In 2000, that was far out of reach.

So Kitaev asked: can the physics itself do the protecting?

Here is a first idea. Let each qubit be a site that is either empty, or holds one electron.

Now a bit flip would mean creating or destroying an electron out of nothing. Charge conservation forbids that. Even in a superconductor, where charge is only conserved modulo two, the parity, even or odd, is protected.

The only loophole is an electron hopping from one site to another, and that can be suppressed by putting the sites far apart, with an energy gap in between.

But phase errors survive. Empty and full sites have different energies, so they pick up different phases. The operator a†a, asking "is this site full?", is exactly a phase error, and nothing local stops it.

## 2 · Splitting a fermion in two

Here comes the mathematical trick. Each site has an annihilation operator a, and a creation operator a†.

Just as a complex number splits into a real and an imaginary part, we can split a in two. c₁ equals a plus a†. And c₂ equals a minus a†, over i.

These are Majorana operators. Each one is its own antiparticle, c dagger equals c. Each squares to one, and different ones anticommute.

Going backwards, a is c₁ plus i c₂, over two. Two Majoranas make one ordinary fermion.

Now rewrite the dangerous phase error, a†a. In Majoranas, it is one half, times one plus i c₁ c₂.

It needs both halves at once. If c₁ and c₂ lived on different, distant sites, this error would require them to interact, and that could be avoided.

And a single Majorana can never appear alone in any physical Hamiltonian, because it would change the fermion parity. An isolated Majorana is immune to every kind of local error.

The catch: Majoranas are not lying around in solids. The goal of the paper is to build a Hamiltonian where they emerge as low energy degrees of freedom, and surprisingly, ordinary non-interacting electrons are enough.

The organizing idea is pairing. Any quadratic Hamiltonian can be written as i over four, times a sum of A l m, c l c m. Its ground state pairs the Majoranas up. Usually all of them. But sometimes, a few are left over.

## 3 · A toy model

Kitaev's toy model is a chain of L sites, a quantum wire, lying on the surface of a three-dimensional superconductor.

Two ingredients are needed. First, superconductivity. The symmetry behind charge conservation, U one, must be broken down to a simple sign flip, Z two. A Majorana mixes a with a dagger, so only a Z two symmetry can leave it alone.

Second, only one spin direction should be present. Think of spinless electrons. In a footnote, Kitaev notes that this takes triplet, p-wave pairing in the superconductor underneath.

The Hamiltonian has three terms. The hopping, w, lets an electron jump between neighbouring sites.

The chemical potential, mu, sets the energy cost of filling a site.

And the superconducting pairing, delta, creates or destroys pairs of electrons on neighbouring sites. This is the term that breaks charge conservation.

Now rewrite everything in Majoranas. Every site splits into a blue half and a gold half.

The chemical potential couples the two halves of the same site. Hopping and pairing combine into bonds between neighbours. w plus delta couples each gold to the next blue, and delta minus w couples each blue to the next gold.

Now, let's look at two special cases.

## 4 · Two ways to pair

Case one. No hopping, no pairing, and a negative chemical potential. Only the on-site term survives.

So each blue Majorana pairs with the gold partner on its own site. Every site is simply empty. It's boring, and completely ordinary.

Case two. Set mu to zero, and make the hopping equal to the pairing. Now the on-site term vanishes, and so does the bond from blue to the next gold.

What's left is H equals i w, times the sum of c₂ⱼ c₂ⱼ₊₁. Each gold Majorana pairs with the blue one on the next site.

The pairing has slid over by one. And now, look at the ends.

The very first Majorana, c₁, and the very last one, c₂L, appear nowhere in the Hamiltonian. They are unpaired.

Each bonded pair forms a new fermion, a tilde j, stretched across two sites and costing energy two w. The ground state leaves all of them empty.

But the two leftovers, b prime and b double prime, form one more fermion mode, and it costs zero energy. So there are two ground states, psi zero and psi one, with exactly the same energy.

They differ in fermion parity. One has an even number of electrons, the other an odd number.

Here's the subtle part. In the bulk, the two phases look identical. One is just a relabeling of the other, shifting every Majorana over by one. Only at the ends does the difference show.

Or, as Kitaev puts it: you cannot cut a physical site in half. If you could, both kinds of boundary would be possible.

## 5 · A qubit with no address

So here is our qubit. Empty or occupied, it lives in a single fermion mode built from two Majoranas at opposite ends of the wire.

Try to read it locally. Noise near the left end can only touch b prime. But b prime alone changes parity, so it cannot appear in any Hamiltonian. To learn anything, you need b prime times b double prime. You must touch both ends at once.

A bit flip needs a whole electron to appear or vanish. Parity forbids it. A phase error needs the two ends to talk. Distance and the energy gap suppress it.

Both kinds of error are blocked, not by clever correction, but by geometry. This is what the abstract means by a qubit intrinsically immune to decoherence.

But fine-tuned special points rarely survive in the real world. What happens away from w equals delta, and mu equals zero?

## 6 · Gaps and phases

To find out, look at the bulk. In an infinite wire, an excitation with momentum q costs energy epsilon of q: the square root of, two w cos q plus mu, squared, plus four delta squared, sine squared q.

Start in the case we just solved. There is a healthy gap: no excitations anywhere near zero energy.

Now raise mu. The gap shrinks,

and closes exactly when mu reaches two w.

Past that point, it opens again, but we are now in the trivial phase.

There is no way from one phase to the other without closing the gap. That is the hallmark of a topological phase transition.

Mapping it out: the phase with unpaired Majoranas fills the whole region where two w exceeds mu in size, as long as delta is not zero. Everywhere else, the wire is trivial.

And along the line delta equals zero, inside that region, the wire is just a normal metal, with no gap at all. Pairing, however weak, is what opens the gap.

## 7 · Zero modes at the ends

Are the end Majoranas still there away from the sweet spot? Kitaev looks for zero energy modes built from powers of two numbers, x plus and x minus.

In the trivial region, one root is larger than one, and the other smaller. A mode that decays from an edge cannot then satisfy the boundary condition. So there are no zero modes.

In the topological region, both roots are smaller than one. b prime decays away from the left end, and b double prime from the right.

Here are the real modes, found by diagonalizing a forty site chain. As mu creeps toward two w, they spread deeper into the wire, but they stay pinned to the ends.

In a finite wire, the two tails overlap ever so slightly. That gives a tiny effective coupling: H effective equals i over two, t, b prime, b double prime.

And t falls off exponentially with the length of the wire: t is proportional to e to the minus L over l zero. On a logarithmic scale, a straight line.

Make the wire a few correlation lengths longer, and the splitting drops by orders of magnitude. This even survives weak interactions: t is just the amplitude for a quasiparticle to tunnel the full length of a gapped wire.

## 8 · The Majorana number

Now Kitaev asks a deeper question. Forget the toy model. Given any gapped one-dimensional superconductor, how can you tell whether it hosts unpaired Majoranas?

Define the Majorana number, M. It is minus one if there are unpaired Majoranas, and plus one if not. Two parallel chains can pair their end Majoranas and cancel, so M multiplies.

Remarkably, you don't even need ends. Close the chain into a loop, and look at the parity of its unique ground state.

Take two loops, of lengths L₁ and L₂. Cut them open, and reconnect them into one big loop.

Wherever two ends meet, a coupling u fixes the sign of i b double prime b prime. Reconnecting swaps which end meets which, and that costs exactly one factor of M.

So M is written into the bulk itself. For free fermions, the ground state parity is the sign of a Pfaffian: a square root of a determinant, which remembers the sign that a determinant forgets.

Fourier transform the loop. Every momentum q pairs up with minus q, and each pair contributes a positive determinant. Only q equals zero and q equals pi are their own partners.

The result: M equals the sign of the Pfaffian at zero, times the sign of the Pfaffian at pi. A topological invariant, read off from just two points in the Brillouin zone.

For our chain, the Pfaffian at zero is minus mu minus two w. At pi, it is minus mu plus two w. Their product is negative exactly when two w beats mu. The phase diagram falls right out.

## 9 · Count the Fermi points

When superconductivity is weak, this becomes beautifully simple. Turn off delta and look at the ordinary electron band.

M equals minus one, to the power nu of pi minus nu of zero. And that is just the number of Fermi points between zero and pi.

So count them. One Fermi point in each half of the Brillouin zone: odd. Add any small gap, and you get unpaired Majoranas.

Lower the band until it no longer crosses: zero Fermi points, even, trivial.

And here is why real materials make this hard. Electrons have spin. Spin up and spin down usually give identical bands, so every Fermi point comes in a pair. Always even.

Each spin component counts separately. To get an odd number, the spin degeneracy must be lifted, which needs broken time reversal symmetry. Spin-orbit coupling alone will not do.

Kitaev speculates that a magnetic field plus a charge density wave might gap out just one spin species, leaving an odd count behind.

## 10 · The 4π Josephson effect

How could anyone actually see these Majoranas? The paper ends with a striking proposal.

Remember the superconducting phase, theta. The Majorana operators carry a factor e to the i theta over two. Wind theta by two pi, and every Majorana flips its sign.

The Hamiltonian comes back to itself. The ground states don't, quite. The winding applies the operator V, minus i b prime b double prime, which is equivalent to moving an electron from one end of the chain to the other.

Now build a Josephson junction out of the wire: two superconductors, with a phase difference theta between them.

Advance theta by two pi, and a single fermionic quasiparticle is carried to the junction. The Majoranas switch from psi zero to psi one. The system is now on the other branch.

So the Josephson energy is two-valued, and the current is four pi periodic, instead of the usual two pi. A fingerprint of unpaired Majoranas.

For a finite wire, the two branches almost cross at theta equals pi, split only by the tiny t. And the paper even sketches how phase slips on a small island might be switched on and off to implement quantum gates.

## Legacy & recap

That's the whole paper: sixteen pages, and a model its author called rather unrealistic. It launched a field.

A decade later, theorists showed how semiconductor nanowires, with strong spin-orbit coupling, a magnetic field, and a nearby superconductor, could realize Kitaev's chain. Experiments ever since have hunted for its zero energy signatures, with exciting hints, and lively debate.

Majorana based topological qubits remain one of the most ambitious routes to a quantum computer.

So, to recap. Split every electron into two Majoranas.

Pair them across sites, instead of within them.

Two halves are left stranded at the ends, sharing one qubit that no local noise can touch.

And whether a wire can do this is decided by a single sign, the Majorana number, hidden in its bulk.

Protection, not from engineering, but from topology. That is the beauty of Kitaev's idea.
