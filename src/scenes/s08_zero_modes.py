from manim import *
from src.base import NarratedScene
from src.style import *
from src.physics import zero_modes, splitting_vs_length


def roots(mu, w, d):
    disc = complex(mu * mu - 4 * w * w + 4 * d * d)
    s = np.sqrt(disc)
    return (-mu + s) / (2 * (w + d)), (-mu - s) / (2 * (w + d))


class S08ZeroModes(NarratedScene):
    SID = "s08"

    def construct(self):
        w, d = 1.0, 0.6
        mu = ValueTracker(3.0)

        # 0 ansatz
        self.beat(0)
        card = chapter_card(7, "Zero modes at the ends")
        self.play(FadeIn(card, shift=UP * 0.3), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(card), run_time=0.6)
        ans = M(r"b' = \sum_j \left(\alpha'_+ x_+^{\,j} + \alpha'_- x_-^{\,j}\right) c_{2j-1}", size=36)
        xr = M(r"x_\pm = \frac{-\mu \pm \sqrt{\mu^2 - 4w^2 + 4|\Delta|^2}}{2(w + |\Delta|)}", size=36)
        VGroup(ans, xr).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.4)
        self.play(Write(ans), run_time=1.6)
        self.fill(Write(xr), lead=0.2)

        # complex plane with roots
        plane = ComplexPlane(x_range=[-2.2, 2.2], y_range=[-1.4, 1.4], x_length=4.4, y_length=2.8,
                             background_line_style={"stroke_color": FAINT, "stroke_width": 1},
                             axis_config={"stroke_color": DIM}).shift(LEFT * 3.8 + DOWN * 1.6)
        unit = Circle(radius=plane.n2p(1)[0] - plane.n2p(0)[0], color=INK, stroke_width=2).move_to(plane.n2p(0))

        def rdots():
            a, b = roots(mu.get_value(), w, d)
            g = VGroup()
            for z, c in ((a, BLUE_M), (b, GOLD_M)):
                g.add(Dot(plane.n2p(z), color=c, radius=0.09))
            return g
        rd = always_redraw(rdots)

        def status():
            a, b = roots(mu.get_value(), w, d)
            inside = int(abs(a) < 1) + int(abs(b) < 1)
            txt = "both inside: zero modes" if inside == 2 else "one outside: no zero mode"
            col = PINK_M if inside == 2 else DIM
            return VGroup(M(r"\mu = %.2f" % mu.get_value(), size=32, color=GREEN_M),
                          T(txt, 26, col)).arrange(DOWN, buff=0.15).next_to(plane, RIGHT, 0.5)
        st = always_redraw(status)
        uc = T("|x| = 1", 22, DIM).next_to(unit, UP, 0.05).shift(RIGHT * 0.9)

        # 1 trivial region
        self.beat(1)
        self.play(Create(plane), Create(unit), FadeIn(uc), run_time=1.0)
        self.add(rd, st)
        self.play(mu.animate.set_value(2.6), run_time=2.0)
        self.fill(mu.animate.set_value(3.2), lead=0.2)

        # 2 topological region
        self.beat(2)
        self.play(mu.animate.set_value(1.0), run_time=2.6)
        self.fill(mu.animate.set_value(0.5), lead=0.2)

        # 3 real wavefunctions from diagonalization
        self.beat(3)
        L = 40
        ax = Axes(x_range=[0, L, 10], y_range=[0, 0.5, 0.1], x_length=6.2, y_length=2.8,
                  axis_config=dict(color=DIM, include_tip=False, include_ticks=False)).shift(RIGHT * 3.4 + DOWN * 1.7)
        axl = T("site j", 22, DIM).next_to(ax.x_axis, DOWN, 0.1)
        bw = ax.x_length / L

        def bars():
            _, l, r = zero_modes(L, mu.get_value(), w, d)
            g = VGroup()
            for j in range(L):
                for val, col in ((l[j], PINK_M), (r[j], PURPLE_M)):
                    h = min(val, 0.5) * ax.y_length / 0.5
                    if h > 0.004:
                        g.add(Rectangle(width=bw * 0.8, height=h, stroke_width=0, fill_color=col,
                                        fill_opacity=0.85).move_to(ax.c2p(j + 0.5, 0), aligned_edge=DOWN))
            return g
        self.play(FadeOut(st), FadeOut(VGroup(ans)), xr.animate.scale(0.8).to_edge(UP, buff=0.3), run_time=0.6)
        self.remove(st)
        mu_ro = always_redraw(lambda: M(r"\mu = %.2f" % mu.get_value(), size=32, color=GREEN_M).next_to(plane, UP, 0.2))
        self.add(mu_ro)
        self.play(Create(ax), FadeIn(axl), run_time=0.8)
        br = always_redraw(bars)
        lb = VGroup(M("b'", size=34, color=PINK_M).next_to(ax.c2p(2, 0.45), UP, 0.05),
                    M("b''", size=34, color=PURPLE_M).next_to(ax.c2p(38, 0.45), UP, 0.05))
        self.add(br)
        self.play(FadeIn(lb), run_time=0.6)
        self.play(mu.animate.set_value(1.7), run_time=4.0, rate_func=there_and_back_with_pause)
        self.fill(mu.animate.set_value(1.5), lead=0.2)

        # 4 overlap: effective coupling
        self.beat(4)
        heff = M(r"H_{\text{eff}} = \frac{i}{2}\, t\, b' b''", size=48).shift(LEFT * 3.4 + UP * 1.0)
        self.play(FadeOut(VGroup(plane, unit, uc)), FadeOut(rd), FadeOut(mu_ro), run_time=0.6)
        self.play(Write(heff), run_time=1.4)
        mid = Rectangle(width=ax.c2p(26, 0)[0] - ax.c2p(14, 0)[0], height=0.6, color=PINK_M).move_to(ax.c2p(20, 0.04))
        ov = T("tiny overlap", 24, PINK_M).next_to(mid, UP, 0.1)
        self.fill(Create(mid), FadeIn(ov), lead=0.2)

        # 5 exponential splitting
        self.beat(5)
        self.play(FadeOut(VGroup(ax, axl, lb, mid, ov)), FadeOut(br), run_time=0.6)
        Ls = np.arange(4, 41, 2)
        s = splitting_vs_length(Ls, 1.0, w, d)
        lg = np.log10(s)
        lax = Axes(x_range=[0, 42, 10], y_range=[-16, 1, 5], x_length=6.0, y_length=4.0,
                   axis_config=dict(color=DIM, include_tip=False),
                   y_axis_config=dict(include_numbers=False)).shift(RIGHT * 3.0 + DOWN * 0.6)
        yl = M(r"\log_{10} t", size=30, color=DIM).next_to(lax.y_axis, UP, 0.1)
        xl = M("L", size=30, color=DIM).next_to(lax.x_axis, RIGHT, 0.1)
        ylabs = VGroup(*[M(f"{v}", size=22, color=DIM).next_to(lax.c2p(0, v), LEFT, 0.1) for v in (0, -5, -10, -15)])
        pts = VGroup(*[Dot(lax.c2p(L_, max(v, -16)), color=PINK_M, radius=0.06) for L_, v in zip(Ls, lg)
                       if v > -15.5])
        self.play(Create(lax), FadeIn(yl), FadeIn(xl), FadeIn(ylabs), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in pts], lag_ratio=0.08), run_time=2.0)
        good = lg > -15
        k, c = np.polyfit(Ls[good], lg[good], 1)
        fit = lax.plot(lambda x: k * x + c, x_range=[3, min(41, -15.5 / k if k < 0 else 41)], color=INK, stroke_width=2)
        law = M(r"t \propto e^{-L/l_0}", size=48, color=PINK_M).next_to(heff, DOWN, 0.6)
        self.play(Create(fit), Write(law), run_time=1.4)
        self.fill(Wait(), lead=0.1)

        # 6 exponential protection
        self.beat(6)
        l0 = -1 / (k * np.log(10))
        l0t = M(r"l_0 \approx %.1f \text{ sites}" % l0, size=34, color=DIM).next_to(law, DOWN, 0.35)
        self.play(FadeIn(l0t), run_time=0.8)
        tun = VGroup(T("t = amplitude to tunnel", 24), T("across the whole wire", 24)).arrange(DOWN, buff=0.1).next_to(l0t, DOWN, 0.5)
        tun2 = T("(survives weak interactions)", 22, DIM).next_to(tun, DOWN, 0.15)
        self.play(FadeIn(tun), run_time=1.0)
        self.fill(FadeIn(tun2), lead=0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
