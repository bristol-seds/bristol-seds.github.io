---
layout: post
title:  "Reflow Soldering"
categories: pico-tracker soldering reflow
asset_path: /assets/posts/pico-reflow/
---

#### Surface mount boards, such as the one used by the [pico tracker](/pico-tracker/balloon/2014/08/01/pico-tracker.html), are essential for modern electronics. But how are UBSEDS producing "professional quality" boards at very low volumes and for low cost?

<!-- more -->

# The Board

A run of two-sided Printed Circuit Boards (PCB) can be obtained from a number of suppliers relatively cheaply (< £100) if you're prepared to wait out a 2 - 3 week lead time. There are [too many suppliers to mention](https://wiki.london.hackspace.org.uk/view/Guides:PCB_Fabrication#Fab_Houses), but our two personal favourites are [hackvana](http://www.hackvana.com/store/) and [pcb-pool](http://www.pcb-pool.com/ppuk/index.html). Hackvana gives a great personal service and is probably the lowest cost, while pcb-pool are super-reliable and often deliver ahead of time. In either case we always get a laser cut stencil as it'll be needed later.

Both of these suppliers will work with 0.3mm drill and 6/6mil track/gap as standard, so this is what we've been using for our boards. That's more than enough for most SOIC/QFP/QFN packages, and might only become a problem if you're trying to do [something silly like BGA escape routing](http://hforsten.com/making-embedded-linux-computer.html).

You really can't etch this quality of board at home or in a simple lab. It's much cheaper to let someone with a robot do it for you. Honest!

# The Paste

Reflow soldering works by precisely applying the solder as a [paste](http://en.wikipedia.org/wiki/Solder_paste) ahead of time, and then heating it up later. To do this you'll need to get youself some of this magical paste, and we've always used [Beta Layout](http://www.beta-estore.com/rkuk/order_product_details.html?wg=1&p=18). There are other suppliers like [Farnell](http://uk.farnell.com/jsp/search/browse.jsp?N=203806) but to ensure you get your paste in top-notch condition they might ship it to you in a refrigerated articulated lorry - which is probably not what you want. One pot will probably last you a couple of years.

# The Process

I must start by saying that [SparkFun](https://www.sparkfun.com/tutorials/category/2) have a set of great tutorials on this and you should probably check them out afterwards. But on with our assembly:

## <small>Tape down the board</small>

![Taped down board]({{ "board.jpg" | prepend: page.asset_path }})

What more can I say? You don't want the board moving about while you're trying to apply the paste. Masking tape works wonderfully as it doesn't leave a residue.

## <small>Tape down the stencil</small>

![Stencil Taped on top]({{ "stencil.jpg" | prepend: page.asset_path }})

Carefully line up the stencil and tape it down too. Use some unused PCB boards of the same thickness to create a flat surface around the board you're working on - that stops the stencil from flexing when you tape it down. You'll develop various tricks for getting the alignment right at this stage: I personally find the vias at the corners of QFN ground pads make particuarly good alignment points.

There are more sophisticated ways of aligning the stencil, and the best of the bunch is probably [stencil8](http://www.hoektronics.com/2012/10/27/super-simple-smt-stencil8/). Definitely worth the investment if you're doing lots of boards like this.

## <small>Apply the paste</small>

Use a squeege! You can get one of [them from beta layout too](http://www.beta-estore.com/rkuk/order_product_details.html?wg=1&p=23). Just make sure you get the paste down all the holes in the stencil.

## <small>Remove the stencil</small>

Try to make sure you don't smudge the paste you've just applied so neatly. If you do - no matter - just wipe off the paste and start over.

Always clean your stencil! Isopropyl alcohol is ideal, but a blast of hot water is surprisingly effective. Keep going until there's no paste left in the holes.

Your board should then look something like this:

![Board with Paste]({{ "paste.jpg" | prepend: page.asset_path }})

## <small>Add the components</small>

You'll probably want to get some tweezers, especially if you're trying to place things like this 0402 inductor.

![0402 Inductor]({{ "inductor.jpg" | prepend: page.asset_path }})

The 0402 designation means this inductor is about 0.04 x 0.02 inches - which for the imperially challenged is exactly 1 x 0.5 mm. You'll probably want plastic tweezers for this one as wirewound inductors like to stick to metal tweezers.

## <small>Zooming in..</small>

![Completed RF stage]({{ "rf-stage-paste-complete.jpg" | prepend: page.asset_path }})

You can really see the components! Don't worry if the components aren't prefectly aligned at this stage: When you reflow the surface tension of the molten solder will pull them into place.

## <small>Zooming in further..</small>

![Close up photo of solder paste]({{ "paste-closeup.jpg" | prepend: page.asset_path }})

Now you can see how the solder paste manages to be solder and paste at the same time. It's really just lots of metal balls suspended in some sticky resin. Awesome!

## <small>Baking</small>

You could theortically do this in your main oven, or even in a [frying pan](https://www.sparkfun.com/tutorials/59#Hot Plate Reflowing). But that's probably not advisable (Read: please please don't do this) and you can easily aquire [a toaster oven](http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=toaster+oven) for not very much money. Once you've used it for soldering, consider it contaminated and don't put food in it!

Here's one setup in a Bristol basement:

![Solder oven]({{ "oven.jpg" | prepend: page.asset_path }})

You can buy / make reflow controllers that attempt to regulate the temperature profile inside the oven. Or you can simply heat up the board until the solder melts at about 230°C - the phase change is easy to spot with a little practice - and then cool off the board straight away.

Try not to disturb the board too much while it's cooling as the crystal structures are still forming. But if you got to this stage successfully you're likely to have a lovely surface mount board at the end.

![Pico Tracker]({{ "pico-tracker.jpg" | prepend: page.asset_path }})

# Conculsions

With a little practice we've been building a board like this in two or three hours. It would be much less time-consuming if we had tools such as a [pick and place machine](http://en.wikipedia.org/wiki/SMT_placement_equipment) but on a student budget this is an excellent method of achieving "professional quality" boards in very small quantities.

Producing surface mount assemblies like this also reduces some mechanical reliability issues. If the board is reflowed correctly every connection on the board will be a good solder joint that is far superior to a connector pin. This is a definite advantage for spaceflight where high mechanical and themal stresses will be common.